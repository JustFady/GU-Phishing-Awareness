# Gonzaga Phishing Awareness

This project is a static phishing-awareness training demo. It is designed to help students, staff, and faculty understand how credential phishing works, why fake password-reset pages can be convincing, and what warning signs to look for before entering account information.

Live demo: https://justfady.github.io/GU-Phishing-Awareness/

## What Is Phishing?

Phishing is a social engineering attack where an attacker pretends to be a trusted person or organization to trick someone into taking an unsafe action. Common goals include stealing passwords, collecting multi-factor authentication codes, installing malware, or convincing someone to send money or sensitive information.

Credential phishing is especially common in university environments because one account can provide access to email, learning systems, cloud storage, payroll portals, and other internal services.

## How This Type of Attack Works

A typical password-reset phishing attack follows this pattern:

1. The attacker sends an email that appears to come from a trusted university department, IT support desk, or automated account system.
2. The email creates urgency, such as claiming the account will expire, access will be suspended, or a password must be updated immediately.
3. The message includes a link to a fake login or password-change page.
4. The page uses familiar branding, colors, logos, and wording to look legitimate.
5. The victim enters an email address and password.
6. A real phishing site would send those credentials to the attacker, who may try to access the account quickly before the victim notices.

This demo stops before that final harmful step. It does not send credentials to a server, store submissions, write logs, or display raw password values.

## Example Phishing Email

```text
Subject: Action Required: Gonzaga Account Password Update

Dear Gonzaga Community Member,

Our records show that your university account password is scheduled to expire today.
To avoid interruption to email, Canvas, and campus services, please update your
password using the secure account portal below:

Update Password: https://example.com/gonzaga-account-update

If your password is not updated within 24 hours, your account access may be
temporarily suspended.

Thank you,
Gonzaga Account Services
```

This email is suspicious because it creates urgency, uses a generic greeting, threatens account suspension, and sends the recipient to a link that should be carefully verified before use.

## Warning Signs

- The email pressures you to act immediately.
- The sender address does not match the official organization domain.
- The link destination does not match the service it claims to represent.
- The message asks for a password after you clicked a link in an email.
- The greeting is generic or the wording feels unusual.
- The page looks familiar but the browser address bar is wrong.
- The site asks for more information than needed.

## What To Do Before Entering Credentials

- Check the browser address bar carefully.
- Navigate to the service directly instead of using the email link.
- Use bookmarks or official university pages when possible.
- Be cautious with unexpected password reset requests.
- Report suspicious emails to the appropriate IT or security team.
- If you entered credentials on a suspicious page, change your password from the real account portal and contact support immediately.

## What This Demo Shows

The demo includes:

- A password-reset style page.
- A result page showing what limited information a browser-only page can read.
- Masked password fields with character counts.
- Basic browser-visible metadata such as timestamp, public IP when available, user agent, platform, and timezone.

The demo intentionally does not collect, store, transmit, or reveal raw passwords.

## Project Files

- `index.html` - password-reset simulation page
- `success.html` - browser-only capture report page
- `logs.html` - training notes
- `css/style.css` - site styling
- `assets/` - images and favicon
- `.github/workflows/main.yml` - GitHub Pages deployment workflow

## Local Preview

Open `index.html` directly in a browser, or run a simple static server:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

## Deployment

The site deploys automatically to GitHub Pages whenever changes are pushed to `main`.
