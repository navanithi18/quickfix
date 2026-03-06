import frappe

def before_uninstall():
    """Prevent uninstall if there are submitted Job Cards"""
    if frappe.db.exists("Job Card", {"docstatus": 1}):
        frappe.throw(
            "Cannot uninstall QuickFix because there are submitted Job Cards. "
            "Please cancel or delete them first.",
            frappe.ValidationError
        )