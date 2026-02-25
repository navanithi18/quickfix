site_config.json – Stores configuration specific to a single site (like database name, admin password, etc.). If this file is misconfigured, that particular site may fail to connect to its database.

common_site_config.json – Stores global bench-level settings shared across all sites (like db_host, Redis settings, background worker configs). If you accidentally expose this file publicly with secrets (DB password, Redis credentials), your entire bench and all sites can be compromised.

hooks.py – Defines how the app integrates with Frappe (events, scheduled tasks, overrides, assets). If hooks are wrong, features like background jobs or custom events may not trigger.

desktop.py (inside config folder) – Controls how your module appears in the Frappe Desk UI. If misconfigured, your module tile may not show on the home page.