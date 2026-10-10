# Contributing to the Git Treeline Website

Thanks for your interest in improving the Git Treeline website.

## Getting started

1. Fork and clone the repo
2. Install dependencies:

```bash
npm install
```

3. Start the dev server:

```bash
npm run dev
```

4. Open http://localhost:4321 (or the port set by `PORT`) in your browser — changes hot-reload automatically

## Making changes

- Edit `src/pages/` for page content and `src/layouts/` / `src/components/` for shared UI
- Edit `src/styles/global.css` for styles and Tailwind v4 `@theme` tokens
- Edit `astro.config.mjs` for site and build configuration
- Keep `public/llms.txt` in sync with product copy, commands, config, and version changes (see `CLAUDE.md`)

## Building for production

```bash
npm run check
```

Requires Python 3 in addition to Node.js. This builds into `dist/`, then checks internal links, assets, section anchors, unique page metadata, H1 headings, JSON-LD, sitemap coverage, and release-version consistency. Intentional redirect pages are excluded from content metadata and sitemap checks. Both pull requests and deployment builds run these checks; pull requests do not deploy.

When updating for a release, keep the homepage badge and software metadata, the getting-started upgrade heading, and `public/llms.txt` current. After building, verify them against GitHub's latest release explicitly:

```bash
python3 scripts/check-site.py --latest
```

The default check runs offline. The optional `--latest` check requires GitHub API access and fails if it cannot verify the release. These checks catch structural errors and version drift; CLI examples and product claims still need review against the release notes and CLI help.

## Pull requests

- Keep PRs focused on a single change
- Test locally before submitting
- Describe what changed and why in the PR description

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
