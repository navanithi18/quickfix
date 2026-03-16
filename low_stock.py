import frappe
from frappe.utils import today, getdate

def check_low_stock():
    """Daily low-stock check with idempotency guard."""

    # Idempotency check: has it already run today?
    last_run = frappe.db.get_value(
        "Audit Log",
        {"action": "low_stock_check"},
        "creation",
        order_by="creation desc"
    )

    if last_run and getdate(last_run) == today():
        frappe.log("Low-stock check already ran today. Skipping...")
        return


    parts = frappe.get_all("Spare Part", fields=["name", "stock_qty", "reorder_level"])
    for part in parts:
        if part.stock_qty <= part.reorder_level:
            frappe.log(f"Low stock alert for {part.name}")

    # Record this run in Audit Log
    frappe.get_doc({
        "doctype": "Audit Log",
        "action": "low_stock_check",
        "status": "Completed",
        "owner": "Administrator"
    }).insert()