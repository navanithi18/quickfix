import frappe

def log_change(doc, method):

    if doc.doctype == "Audit Log" or getattr(frappe.flags, "in_audit_log", False):
        return

    frappe.flags.in_audit_log = True

    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": doc.doctype,
        "document_name": doc.name,
        "action": method,
        "user": frappe.session.user,
        "timestamp": frappe.utils.now_datetime()
    }).insert(ignore_permissions=True)

    frappe.flags.in_audit_log = Fals