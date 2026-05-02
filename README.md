# Gonzaga Phishing Awareness

A static phishing-awareness training demo built for GitHub Pages. The site shows how a convincing password reset page can appear, then explains that no information was submitted or stored.

Live site: https://justfady.github.io/GU-Phishing-Awareness/

## Project Purpose

This project is intended for cybersecurity awareness and classroom demonstration use. It helps users recognize suspicious credential prompts while keeping the implementation safe, static, and transparent.

The current version does not send credentials, write logs, run a backend service, or provide downloadable submission data.

After form submission, the result page shows a browser-only capture report with the submitted email address, masked password values with character counts, timestamp, public IP when available, and a small set of browser-visible metadata. Raw password values are intentionally hidden.

## Pages

- `index.html` - password reset simulation page
- `success.html` - browser-only capture report page
- `logs.html` - training notes and static deployment explanation

Each page includes navigation links so users can move between the simulation, result, and training notes.

## Repository Structure

```text
.
├── .github/workflows/main.yml
├── assets/
├── css/style.css
├── index.html
├── success.html
├── logs.html
└── README.md
```

## GitHub Pages Deployment

The repository deploys to GitHub Pages with `.github/workflows/main.yml` whenever `main` is updated. The workflow uploads the repository as a static site and publishes it through the `github-pages` environment.

## Local Preview

Open `index.html` in a browser, or run any static file server from the repository root:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Safety Notes

- No backend server is used.
- No form data is transmitted to this project.
- Raw credentials are not collected.
- Password values are masked immediately and never stored or shown in raw form.
- No logs, databases, or downloadable submission files are created.
- The form redirects in the browser and uses `sessionStorage` only for the temporary capture report.
- Public IP lookup depends on the visitor browser reaching `api.ipify.org`.
- MAC addresses are not available to websites in modern browsers.

## Maintenance

To update the site, edit the static HTML/CSS files, commit the change, and push to `main`. GitHub Actions will publish the update automatically.
