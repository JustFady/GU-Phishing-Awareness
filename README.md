## Gonzaga Phishing Awareness

Static phishing-awareness demo for GitHub Pages.

## Pages

- `index.html` - password-reset simulation
- `success.html` - simulation result page
- `logs.html` - training notes and deployment explanation

Every page includes navigation links to the other pages.

## Deployment

The repository deploys to GitHub Pages with `.github/workflows/main.yml` whenever `main` is updated. The workflow uploads the repository as a static site and publishes it through the `github-pages` environment.

## Local Preview

Open `index.html` in a browser, or run any static file server from the repository root:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Safety

This version has no backend, no database, no log files, no downloads, and no credential collection. The form redirects in the browser only.
