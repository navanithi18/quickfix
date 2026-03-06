import frappe

DEFAULT_SHOP_NAME = "QuickFix Shop"
DEFAULT_MANAGER_EMAIL = "backupnithi@gmail.com"
DEFAULT_LABOUR_CHARGE = 500


def _ensure_default_settings():
    """Ensure singleton values exist even on sites where they were never initialized."""
    if not frappe.db.get_single_value("QuickFix Settings", "shop_name"):
        frappe.db.set_single_value("QuickFix Settings", "shop_name", DEFAULT_SHOP_NAME)

    if not frappe.db.get_single_value("QuickFix Settings", "manager_email"):
        frappe.db.set_single_value(
            "QuickFix Settings",
            "manager_email",
            DEFAULT_MANAGER_EMAIL,
        )

    if frappe.db.get_single_value("QuickFix Settings", "default_labour_charge") is None:
        frappe.db.set_single_value(
            "QuickFix Settings",
            "default_labour_charge",
            DEFAULT_LABOUR_CHARGE,
        )


def after_install():
    """Setup default data after installing QuickFix app"""
    
    # Create default Device Types
    for device in ["Smartphone", "Laptop", "Tablet"]:
        if not frappe.db.exists("Device Type", device):
            frappe.get_doc({
                "doctype": "Device Type",
                "device_type": device,
                "description": f"Default {device} type",
                "average_repair_hours": 2
            }).insert(ignore_permissions=True)

    # Create default QuickFix Settings values in singleton table.
    _ensure_default_settings()

    frappe.msgprint("QuickFix default setup completed successfully!")


def extend_bootinfo(bootinfo):
    """Add QuickFix shop info to bootinfo sent to client"""
    _ensure_default_settings()
    settings = frappe.get_single("QuickFix Settings")
    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email
