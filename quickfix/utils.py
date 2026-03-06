import frappe


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