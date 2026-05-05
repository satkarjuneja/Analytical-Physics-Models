# Contributing

Contributions are welcome: new models, better visualizations, or improvements to existing ones.

## Adding a New Model

1. Create a folder at the repo root using underscores: `My_New_Model/`
2. Add a `README.md` inside it with:
   - What physical system is being modeled
   - The governing equation(s) in LaTeX
   - A screenshot or output description
3. Keep the script self-contained: one file should be runnable on its own
4. Use `numpy` and `matplotlib` where possible to keep dependencies consistent

## Improving an Existing Model

- Fix a bug → just open a PR with a clear description of what was wrong
- Add a visualization → include a screenshot in the PR
- Improve comments/docs → always welcome

## Code Style

- Name variables descriptively — no single letters except loop indices
- Comment magic numbers (what is `3.4`? what units?)
- One script should do one thing


Check the tab for ideas and bugs
