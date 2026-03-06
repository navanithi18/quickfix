import frappe


def _insert_audit_log(action, doctype_name=None, document_name=None):
    # Prevent recursive logging when Audit Log itself is written.
    if getattr(frappe.flags, "in_audit_log", False):
        return

    frappe.flags.in_audit_log = True
    try:
        frappe.get_doc(
            {
                "doctype": "Audit Log",
                "doctype_name": doctype_name,
                "document_name": document_name,
                "action": action,
                "user": frappe.session.user,
                "timestamp": frappe.utils.now_datetime(),
            }
        ).insert(ignore_permissions=True)
    finally:
        frappe.flags.in_audit_log = False


def log_login(login_manager):
    _insert_audit_log(action="Login")


def log_logout(login_manager):
    _insert_audit_log(action="Logout")


def log_change(doc, method):
    if doc.doctype == "Audit Log":
        return

    _insert_audit_log(
        action=method,
        doctype_name=doc.doctype,
        document_name=doc.name,
    )
