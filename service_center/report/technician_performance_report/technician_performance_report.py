# Copyright (c) 2026, navanithi and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff


def execute(filters=None):

    columns = get_columns(filters)
    data = get_data(filters)
    chart = get_chart(data)
    summary = get_report_summary(data)

    return columns, data, None, chart, summary


def get_columns(filters):

    cols = [
        {
            "label": "Technician",
            "fieldname": "technician",
            "fieldtype": "Link",
            "options": "Technician",
            "width": 180
        },
        {
            "label": "Total Jobs",
            "fieldname": "total_jobs",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Completed",
            "fieldname": "completed",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Avg Turnaround Days",
            "fieldname": "avg_days",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Completion Rate %",
            "fieldname": "completion_rate",
            "fieldtype": "Percent",
            "width": 150
        }
    ]

    # Dynamic Device Type Columns
    device_types = frappe.get_all("Device Type", fields=["name"])

    for dt in device_types:
        cols.append({
            "label": dt.name,
            "fieldname": dt.name.lower().replace(" ", "_"),
            "fieldtype": "Int",
            "width": 100
        })

    return cols


def get_data(filters):

    technicians = frappe.get_list(
        "Technician",
        fields=["name"]
    )

    device_types = frappe.get_all("Device Type", fields=["name"])

    data = []

    for tech in technicians:

        job_filters = {
            "assigned_technician": tech.name
        }

        if filters and filters.get("from_date") and filters.get("to_date"):
            job_filters["creation"] = ["between", [filters.get("from_date"), filters.get("to_date")]]

        if filters and filters.get("technician"):
            job_filters["assigned_technician"] = filters.get("technician")

        jobs = frappe.get_list(
            "Job Card",
            filters=job_filters,
            fields=[
                "name",
                "status",
                "device_type",
                "creation",
                "modified",
                "final_amount"
            ]
        )

        total_jobs = len(jobs)

        completed_jobs = [j for j in jobs if j.status == "Delivered"]
        completed = len(completed_jobs)

        revenue = sum([j.final_amount or 0 for j in jobs])

        avg_days = 0
        if completed > 0:
            days = [date_diff(j.modified, j.creation) for j in completed_jobs]
            avg_days = sum(days) / len(days)

        completion_rate = 0
        if total_jobs > 0:
            completion_rate = (completed / total_jobs) * 100

        row = {
            "technician": tech.name,
            "total_jobs": total_jobs,
            "completed": completed,
            "avg_days": avg_days,
            "revenue": revenue,
            "completion_rate": completion_rate
        }

        # Device Type Counts
        for dt in device_types:

            fieldname = dt.name.lower().replace(" ", "_")

            count = len([
                j for j in jobs if j.device_type == dt.name
            ])

            row[fieldname] = count

        data.append(row)

    return data


def get_chart(data):

    labels = []
    total_jobs = []
    completed = []

    for d in data:
        labels.append(d["technician"])
        total_jobs.append(d["total_jobs"])
        completed.append(d["completed"])

    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Total Jobs",
                    "values": total_jobs
                },
                {
                    "name": "Completed",
                    "values": completed
                }
            ]
        },
        "type": "bar"
    }

    return chart


def get_report_summary(data):

    total_jobs = sum([d["total_jobs"] for d in data])
    total_revenue = sum([d["revenue"] for d in data])

    best_technician = None
    best_completed = 0

    for d in data:
        if d["completed"] > best_completed:
            best_completed = d["completed"]
            best_technician = d["technician"]

    summary = [
        {
            "value": total_jobs,
            "label": "Total Jobs",
            "indicator": "Blue"
        },
        {
            "value": total_revenue,
            "label": "Total Revenue",
            "indicator": "Green"
        },
        {
            "value": best_technician,
            "label": "Best Technician",
            "indicator": "Orange"
        }
    ]

    return summary
