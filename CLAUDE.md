# git-treeline website

Astro site for [git-treeline.dev](https://git-treeline.dev). Docs are hand-authored `.astro` files under `src/pages/docs/`.

## LLM context file

`public/llms.txt` is served at `https://git-treeline.dev/llms.txt`. It is a comprehensive, plain-text summary of git-treeline for AI agents and LLMs — covering the product description, core workflow, full CLI reference, config schema, interpolation tokens, and links to all docs pages.

**Any copy update that touches product description, CLI commands, config fields, or feature explanations must also be reflected in `public/llms.txt`.** This includes: new commands, renamed flags, changed config keys, new features, and updated version numbers.

## Version number

The current version badge on the homepage (`src/pages/index.astro`) and in `public/llms.txt` must stay in sync with the latest release.
