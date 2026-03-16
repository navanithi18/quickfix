import frappe
import pyqrcode
from frappe.utils import get_url_to_form


def rename_technician(old_name, new_name):
    frappe.rename_doc(
        "Technician",
        old_name,
        new_name,
        merge=False
    )


def send_urgent_alert(job_card, manager):
    frappe.log_error(
        f"Urgent Job Card {job_card} requires technician assignment",
        f"Alert sent to manager: {manager}"
    )


def get_shop_name():
    shop_name = frappe.db.get_single_value("QuickFix Settings", "shop_name")
    return shop_name or "QuickFix Service Center"


def get_job_card_qr_base64(doc):
    if not doc or not getattr(doc, "name", None):
        return ""

    job_card_url = get_url_to_form("Job Card", doc.name)

    qr = pyqrcode.create(job_card_url)

    return qr.png_as_base64_str(scale=4)

