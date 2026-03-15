import frappe

def get_shop_name():
    """
    Returns shop name from QuickFix Settings
    """
    settings = frappe.get_single("QuickFix Settings")
    return settings.shop_name


def format_job_id(value):
    """
    Prefix Job ID with JOB#
    """
    return f"JOB#{value}"