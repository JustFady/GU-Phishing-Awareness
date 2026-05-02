# Gonzaga Phishing Awareness

A static phishing-awareness training demo for credential safety education, deployed with GitHub Pages.

Live site: https://justfady.github.io/GU-Phishing-Awareness/

## Overview

This project demonstrates how a password reset prompt can appear convincing, then redirects users to a browser-only report that explains what information a phishing page could read. It is intended for cybersecurity awareness, classroom demonstrations, and safe discussion of social engineering risk.

The site is intentionally static. It does not run a backend, transmit form data to this project, write logs, save submissions, or provide downloadable capture files.

## Features

- Gonzaga-themed password reset simulation.
- Browser-only capture report after submission.
- Displays submitted email, masked password values, password character counts, password match status, timestamp, public IP when available, browser user agent, platform, and timezone.
- Keeps raw password values hidden.
- Deploys automatically to GitHub Pages on updates to `main`.

## Pages

- `index.html` - password reset simulation page
- `success.html` - browser-only capture report page
- `logs.html` - training notes and static deployment explanation

Each page includes navigation links so users can move between the simulation, result, and training notes.

## Suggested GitHub Metadata

Description:

```text
Static phishing-awareness training demo for Gonzaga-themed credential prompt education, deployed with GitHub Pages.
```

Topics:

```text
phishing-awareness
cybersecurity
security-awareness
cybersecurity-education
social-engineering
web-security
github-pages
static-site
html
css
javascript
training-demo
```

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
- Raw credentials are not collected, stored, or displayed.
- Password values are masked immediately and never stored or shown in raw form.
- No logs, databases, or downloadable submission files are created.
- The form redirects in the browser and uses `sessionStorage` only for the temporary capture report.
- Public IP lookup depends on the visitor browser reaching `api.ipify.org`.
- MAC addresses are not available to websites in modern browsers.

## Maintenance

To update the site, edit the static HTML/CSS files, commit the change, and push to `main`. GitHub Actions will publish the update automatically.
