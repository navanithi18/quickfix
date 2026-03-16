import frappe

def after_install():
    """Setup default data after installing QuickFix app"""

    # Create default Device Types
    for device in ["Smartphone", "Laptop", "Tablet"]:
        if not frappe.db.exists("Device Type", {"device_type": device}):
            frappe.get_doc({
                "doctype": "Device Type",
                "device_type": device,
                "description": f"Default {device} type",
                "average_repair_hours": 2
            }).insert(ignore_permissions=True)

    # Create default QuickFix Settings
    if not frappe.db.exists("QuickFix Settings", "QuickFix Settings"):
        frappe.get_doc({
            "doctype": "QuickFix Settings",
            "shop_name": "QuickFix Shop",
            "manager_email": "backupnithi@gmail.com",
            "default_labour_charge": 500,
            "low_stock_alert_enabled": 1
        }).insert(ignore_permissions=True)

    frappe.msgprint("QuickFix default setup completed successfully!")


def extend_bootinfo(bootinfo):
    """Add QuickFix shop info to bootinfo sent to client"""

    settings = frappe.get_single("QuickFix Settings")

    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email