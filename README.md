🚀 CI/CD test Wed May  7 09:08:41 CEST 2025
🚀 CI/CD test Wed May  7 09:13:13 CEST 2025 v2
🚀 CI/CD test Wed May  7 09:13:35 CEST 2025 v2
🚀 CI/CD test Wed May  7 09:21:06 CEST 2025 v3

Email for contact form
---------------------
- New app `apps.site_email` sends a notification when the contact form is submitted. It is fire-and-forget and logs failures without breaking the redirect.
- Default backend is `django.core.mail.backends.console.EmailBackend`, so local runs print emails to the console; pytest uses the locmem backend.
- Configure recipients via `SITE_EMAIL_RECIPIENTS` (comma-separated). `DEFAULT_FROM_EMAIL` is used as the sender and reply-to is set to the user's email.
- Example `.env` snippet:
  ```
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  DEFAULT_FROM_EMAIL=noreply@example.com
  SITE_EMAIL_RECIPIENTS=owner@example.com,backup@example.com
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_HOST_USER=user@example.com
  EMAIL_HOST_PASSWORD=secret
  EMAIL_USE_TLS=True
  EMAIL_TIMEOUT=10
  ```
- Quick test locally (prints to stdout): `pytest apps/contact_messages/tests/test_submit_view.py::test_submit_sends_email_notification apps/site_email/tests/test_services.py::test_send_contact_message_email_sends`

Logging
-------
- New `apps.site_logging` provides `get_logging_config`; dev/prod/test now use it so errors bubble to console and, when `DEBUG=False` and `ADMINS` is set, also email admins via `AdminEmailHandler`.
- Configure recipients via `ADMIN_EMAILS` (comma-separated) and optional `ADMIN_NAME`; set `SERVER_EMAIL` if you need a custom from-address for error emails.
- Example `.env.prod` snippet:
  ```
  ADMIN_EMAILS=owner@example.com,ops@example.com
  ADMIN_NAME=Site Monitor
  SERVER_EMAIL=errors@example.com
  ```

SEO
---
- New `apps.site_seo` adds `/sitemap.xml` and `/robots.txt` (auto-includes the sitemap URL). Sitemaps cover static pages and property detail pages.
- Templates now emit canonical URLs, Open Graph/Twitter meta tags, and JSON-LD Organization data when company info is present.
- Configure in `.env`:
  ```
  SITE_URL=https://www.example.com
  SITE_OG_IMAGE=https://www.example.com/static/img/og-cover.png  # optional
  ```
- To verify locally: `pytest apps/site_seo/tests/test_seo_endpoints.py` and open `http://localhost:8000/sitemap.xml` / `http://localhost:8000/robots.txt`.
