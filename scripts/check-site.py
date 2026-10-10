#!/usr/bin/env python3
"""Check the built site's links, metadata, sitemap, and release references."""

import argparse
from collections import Counter, defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


SITE = "https://git-treeline.dev"
RELEASES = "https://github.com/git-treeline/cli/releases/tag/v"
VERSION = r"\d+\.\d+\.\d+(?:-[\w.-]+)?(?:\+[\w.-]+)?"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.references = []
        self.metadata = defaultdict(list)
        self.canonicals = []
        self.titles = []
        self.headings = []
        self.anchors = []
        self.jsonld = []
        self.text = []
        self.non_content_tag = None
        self.redirect = False
        self.capture = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.non_content_tag = tag
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "meta":
            self.redirect |= attrs.get("http-equiv", "").lower() == "refresh"
            self.metadata[attrs.get("name", attrs.get("property"))].append(attrs.get("content", ""))
        if tag == "a" and attrs.get("href"):
            self.references.append(attrs["href"])
        if tag in ("script", "img", "source", "video", "audio", "iframe", "input") and attrs.get("src"):
            self.references.append(attrs["src"])
        if tag == "video" and attrs.get("poster"):
            self.references.append(attrs["poster"])
        if tag == "link":
            relations = attrs.get("rel", "").split()
            if "canonical" in relations:
                self.canonicals.append(attrs.get("href", ""))
            if set(relations) & {"stylesheet", "icon", "preload", "modulepreload"} and attrs.get("href"):
                self.references.append(attrs["href"])
        if self.capture is None and (tag in ("title", "h1", "h2", "a") or
                                     tag == "script" and attrs.get("type") == "application/ld+json"):
            self.capture = (tag, attrs, [])

    def handle_data(self, data):
        if self.non_content_tag is None:
            self.text.append(data)
        if self.capture:
            self.capture[2].append(data)

    def handle_endtag(self, tag):
        if tag == self.non_content_tag:
            self.non_content_tag = None
        if not self.capture or self.capture[0] != tag:
            return
        _, attrs, parts = self.capture
        content = " ".join("".join(parts).split())
        if tag == "title":
            self.titles.append(content)
        elif tag == "script":
            self.jsonld.append("".join(parts))
        elif tag == "a":
            self.anchors.append((attrs.get("href", ""), content))
        else:
            self.headings.append((tag, attrs.get("id"), content))
        self.capture = None


def route_for(path):
    route = "/" + path.as_posix()
    if route.endswith("/index.html"):
        route = route[:-len("index.html")]
    return route.rstrip("/") or "/"


def schema_versions(value):
    if isinstance(value, dict):
        if "softwareVersion" in value:
            yield str(value["softwareVersion"])
        for child in value.values():
            yield from schema_versions(child)
    elif isinstance(value, list):
        for child in value:
            yield from schema_versions(child)


def check_site(root, latest=False):
    issues = []
    pages = {route_for(path.relative_to(root)): Page(path) for path in root.rglob("*.html")}
    content_pages = {route: page for route, page in pages.items() if not page.redirect}
    if not content_pages:
        return [f"{root}: no content pages found; run npm run build first"], 0

    def issue(route, message):
        issues.append(f"{route}: {message}")

    metadata_values = {name: defaultdict(list) for name in ("title", "description", "canonical")}
    for route, page in content_pages.items():
        base = SITE + route + ("/" if route != "/" and not route.endswith(".html") else "")
        for reference in page.references:
            url = urlparse(urljoin(base, reference))
            if url.scheme not in ("http", "https") or url.netloc != urlparse(SITE).netloc:
                continue
            target_route = unquote(url.path).rstrip("/") or "/"
            if target_route.endswith("/index.html"):
                target_route = target_route[:-len("/index.html")] or "/"
            target = pages.get(target_route)
            if target is not None:
                if url.fragment and unquote(url.fragment) not in target.ids:
                    issue(route, f"missing fragment: {reference}")
            elif not (root / unquote(url.path).lstrip("/")).is_file():
                issue(route, f"missing internal target: {reference}")

        for identifier, count in Counter(page.ids).items():
            if count > 1:
                issue(route, f"duplicate id: {identifier}")
        for name, values in (("title", page.titles), ("description", page.metadata["description"]),
                             ("canonical", page.canonicals)):
            if len(values) != 1 or not values[0].strip():
                issue(route, f"expected one nonempty {name}, found {values}")
            else:
                metadata_values[name][values[0]].append(route)
        if len(page.canonicals) == 1 and page.canonicals[0].rstrip("/") != (SITE + route).rstrip("/"):
            issue(route, f"canonical does not match route: {page.canonicals[0]}")
        headings = [text for tag, _, text in page.headings if tag == "h1"]
        if len(headings) != 1 or not headings[0]:
            issue(route, f"expected one nonempty H1, found {headings}")
        for value in page.jsonld:
            try:
                json.loads(value)
            except json.JSONDecodeError as error:
                issue(route, f"invalid JSON-LD: {error}")

    for name, values in metadata_values.items():
        for value, routes in values.items():
            if len(routes) > 1:
                issue(", ".join(routes), f"duplicate {name}: {value}")

    try:
        locations = [element.text or "" for element in ET.parse(root / "sitemap.xml").iter()
                     if element.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"]
        sitemap_routes = set()
        for location in locations:
            url = urlparse(location)
            if url.scheme != "https" or url.netloc != urlparse(SITE).netloc or url.query or url.fragment:
                issue("sitemap.xml", f"invalid URL: {location}")
            sitemap_routes.add(unquote(url.path).rstrip("/") or "/")
        if len(sitemap_routes) != len(locations):
            issue("sitemap.xml", "duplicate route")
        for route in sorted(set(content_pages) - sitemap_routes):
            issue("sitemap.xml", f"missing content page: {route}")
        for route in sorted(sitemap_routes - set(content_pages)):
            issue("sitemap.xml", f"non-content or missing page: {route}")
    except (OSError, ET.ParseError) as error:
        issue("sitemap.xml", str(error))

    versions = {}

    def record_version(label, values):
        if len(values) != 1:
            issue(label, f"expected one current release version, found {values}")
        else:
            versions[label] = values[0]

    home = content_pages.get("/")
    if home:
        badges = [(href, text) for href, text in home.anchors if re.fullmatch("v" + VERSION, text)]
        record_version("homepage badge", [text[1:] for _, text in badges])
        for href, text in badges:
            if href != RELEASES + text[1:]:
                issue("homepage badge", f"release link disagrees with badge: {href}")
        software_versions = []
        for value in home.jsonld:
            try:
                software_versions.extend(schema_versions(json.loads(value)))
            except json.JSONDecodeError:
                pass
        record_version("homepage softwareVersion", software_versions)
    else:
        issue("/", "homepage missing")
    getting_started = content_pages.get("/docs/getting-started")
    upgrade_versions = []
    if getting_started:
        for _, identifier, text in getting_started.headings:
            if identifier == "upgrading":
                upgrade_versions.extend(re.findall(r"\bv(" + VERSION + r")\b", text))
    record_version("docs upgrading heading", upgrade_versions)
    for route, page in content_pages.items():
        text = " ".join(page.text)
        for index, match in enumerate(re.finditer(r"Verified\s+against\s+CLI\s+v(" + VERSION + r")\b", text), 1):
            record_version(f"{route} verification marker {index}", [match.group(1)])
    try:
        llms = (root / "llms.txt").read_text(encoding="utf-8")
        record_version("llms.txt current version", re.findall(r"^Current version: v(" + VERSION + r")\b", llms, re.M))
        record_version("llms.txt release notes", re.findall(r"^Release notes: " + re.escape(RELEASES) + "(" + VERSION + r")\s*$", llms, re.M))
    except OSError as error:
        issue("llms.txt", str(error))
    if latest:
        try:
            request = Request("https://api.github.com/repos/git-treeline/cli/releases/latest",
                              headers={"Accept": "application/vnd.github+json", "User-Agent": "git-treeline-website-check"})
            with urlopen(request, timeout=15) as response:
                tag = json.load(response)["tag_name"]
            record_version("GitHub latest release", [tag.removeprefix("v")])
        except (OSError, ValueError, KeyError) as error:
            issue("GitHub latest release", f"could not verify: {error}")
    if len(set(versions.values())) > 1:
        issue("release versions", "; ".join(f"{label}={version}" for label, version in versions.items()))
    return issues, len(content_pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=Path("dist"), help="build directory (default: dist)")
    parser.add_argument("--latest", action="store_true", help="also compare with the latest GitHub release (requires network)")
    args = parser.parse_args()
    issues, page_count = check_site(args.dist, args.latest)
    if issues:
        print("Site checks failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1
    print(f"Site checks passed for {page_count} content pages: links, metadata, sitemap, JSON-LD, and release references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
