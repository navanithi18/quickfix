import frappe
from frappe.utils import today


def send_job_ready_email(job_card):

    doc = frappe.get_doc("Job Card", job_card)

    frappe.sendmail(
        recipients=[doc.customer_email],
        subject="Device Ready for Pickup",
        message=f"""
Hello {doc.customer_name},

Your device repair is completed.

Job Card Number: {doc.name}

Please visit the service center to collect your device.

Thank you,
QuickFix Service Center
"""
    )


def generate_monthly_revenue_report(year):

    months = range(1, 13)
    total_revenue = 0

    for i, month in enumerate(months, 1):

        revenue = frappe.db.sql("""
            SELECT SUM(final_amount)
            FROM `tabJob Card`
            WHERE YEAR(creation)=%s
            AND MONTH(creation)=%s
            AND docstatus=1
        """, (year, month))[0][0] or 0

        total_revenue += revenue

        frappe.publish_progress(
            percent=round(i/12*100),
            title="Generating Revenue Report",
            description=f"Processing month {month}"
        )

    frappe.log_error(
        f"Total revenue for {year}: {total_revenue}",
        "Monthly Revenue Report"
    )


def check_low_stock():

    last_run = frappe.db.get_value(
        "Audit Log",
        {"action": "low_stock_check", "date": today()},
        "name"
    )

    if last_run:
        return

    parts = frappe.get_all(
        "Spare Part",
        filters={"stock_qty": ["<", "reorder_level"]},
        fields=["name", "part_name", "stock_qty"]
    )

    for part in parts:
        frappe.log_error(
            f"Low stock for {part.part_name} (Qty: {part.stock_qty})",
            "Low Stock Alert"
        )

    frappe.get_doc({
        "doctype": "Audit Log",
        "action": "low_stock_check",
        "date": today()
    }).insert(ignore_permissions=True)


def test_failed_job():
    raise Exception("Intentional background job failure")