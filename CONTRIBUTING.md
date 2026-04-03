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

4. Open http://localhost:5173 in your browser — changes hot-reload automatically

## Making changes

- Edit `index.html` for content and structure
- Edit `src/style.css` for custom Tailwind styles
- Edit `tailwind.config.js` for theme tokens

## Building for production

```bash
npm run build
```

Output goes to `dist/`. The GitHub Actions workflow runs this on push to `main`.

## Pull requests

- Keep PRs focused on a single change
- Test locally before submitting
- Describe what changed and why in the PR description

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
