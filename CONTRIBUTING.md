# Contributing to the Git Treeline Website

Thanks for your interest in improving the Git Treeline website.

## Getting started

1. Fork and clone the repo
2. Install the [Tailwind CSS standalone CLI](https://tailwindcss.com/blog/standalone-cli) or use npx
3. Run the dev watcher:

```bash
npx @tailwindcss/cli -i src/input.css -o dist/output.css --watch
```

4. Open `index.html` in your browser

## Making changes

- Edit `index.html` for content and structure
- Edit `src/input.css` for custom styles
- Edit `tailwind.config.js` for theme tokens

The GitHub Actions workflow builds CSS with the Tailwind standalone CLI — no Node.js runtime in production.

## Pull requests

- Keep PRs focused on a single change
- Test locally before submitting
- Describe what changed and why in the PR description

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
