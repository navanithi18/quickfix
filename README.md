In README.md explain in 4 sentences: what each config file is for, and what breaks
if you accidentally put a secret in common_site_config.json

In Frappe, configuration files control how the bench and sites run. The common_site_config.json file stores global settings that apply to all sites in the bench, such as database host or Redis configuration. The site_config.json file is specific to an individual site and contains database credentials and site-level settings. The hooks.py file is used inside an app to define app behavior like fixtures, scheduled tasks, permissions, and custom integrations.
If a secret (like a database password or API key) is accidentally committed inside common_site_config.json, it becomes exposed to anyone who has access to the repository. This can lead to security risks such as unauthorized database access or misuse of external services.
------------------------------------------------------------------------------------------------------------------------------------------------------------
•​ In README.md: list the 4 processes bench start launches (web, worker, scheduler,
socketio) and explain what happens to background jobs if the worker process
crashes

In Frappe, configuration files control how the bench and sites run. The common_site_config.json file stores global settings that apply to all sites in the bench, such as database host or Redis configuration. The site_config.json file is specific to an individual site and contains database credentials and site-level settings. The hooks.py file is used inside an app to define app behavior like fixtures, scheduled tasks, permissions, and custom integrations.

If a secret (like a database password or API key) is accidentally committed inside common_site_config.json, it becomes exposed to anyone who has access to the repository. This can lead to security risks such as unauthorized database access or misuse of external services.
------------------------------------------------------------------------------------------------------------------------------------------------------------
When a browser hits /api/method/quickfix.api.get_job_summary, 
Frappe parses the dotted path and dynamically imports the get_job_summary function from quickfix/api.py. It checks whether the function is marked with @frappe.whitelist(). If valid, Frappe executes the function and returns the result as JSON. The routing is handled internally by Frappe’s API handler.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
When a browser hits /api/resource/Job Card/JC-2024-0001, 
Frappe uses its built-in REST API controller instead of a custom method. It maps the URL to a DocType and document name. The system internally calls frappe.get_doc() and performs permission checks. The document is then returned as JSON if access is allowed.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
When a browser hits /track-job, 

Frappe uses the website routing system. It checks hooks.py for defined routes or matches a corresponding .py or .html file. If a route exists, the related controller or template is executed. This is handled differently from /api/ routes because it is part of the website module.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
The X-Frappe-CSRF-Token is generated when a user session is created and stored server-side. The browser includes this token in POST requests for validation. If the token is missing or incorrect, Frappe rejects the request with a CSRF validation error. This protects the application from cross-site request forgery attacks.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
Running frappe.session.data in bench console shows the current session details. It includes the logged-in user, session ID, roles, login time, and request metadata. This represents the active authenticated session. It helps understand how Frappe tracks user state.
--------------------------------------------------------------------------------------------------------------------------------------------------------------
With developer_mode: 1, if a Python exception occurs in a whitelisted method, the browser receives the full traceback. It includes file names, line numbers, and stack trace details. This helps developers debug issues easily. It is meant only for development environments.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
With developer_mode: 0, the browser receives only a generic “Server Error” message. The detailed traceback is hidden from the user. This is important in production to prevent exposing internal system details. It improves application security.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
In production, hidden errors are stored in Frappe’s log files inside the logs/ directory. They may also appear in the Error Log DocType. Administrators can review these logs for debugging. Errors are not shown to end users.
---------------------------------------------------------------------------------------------------------------------------------------------------------------
If frappe.get_doc("Job Card", name) is called without ignore_permissions, and a Technician who is not assigned tries to access it, Frappe raises a frappe.PermissionError. The request stops during the permission validation step. The user receives a “Not Permitted” response. The check happens at the model layer before returning the document.