import frappe
from frappe.utils import get_last_day, today, getdate

def execute(filters=None):
    if not filters:
        filters = {}

    # Ensure year is an integer
    year = filters.get("year")
    if not year:
        year = getdate(today()).year
    else:
        year = int(year)  # convert string from filter to int

    months = range(1, 13)
    report_data = []

    for i, month in enumerate(months, 1):
        month_str = f"{year}-{month:02d}"
        start_date = f"{month_str}-01"
        end_date = get_last_day(month_str)

        job_cards = frappe.get_all(
            "Job Card",
            filters={
                "docstatus": 1,
                "creation": ["between", [start_date, end_date]]
            },
            fields=["name", "final_amount", "customer_name"]
        )

        month_total = sum(jc.final_amount for jc in job_cards)
        report_data.append([month_str, len(job_cards), month_total])

        # Progress update
        frappe.publish_progress(
            percent=round(i / 12 * 100),
            title="Generating Revenue Report",
            description=f"Processing month {month_str}..."
        )

    columns = ["Month", "Jobs Count", "Total Revenue"]
    return columns, report_data