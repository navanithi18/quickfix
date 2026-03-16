import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class JobCard(Document):

    def before_insert(self):
        settings = frappe.db.get_single_value(
            "QuickFix Settings",
            "default_labour_charge"
        )
        if settings:
            self.labour_charge = settings

    @staticmethod
    def permission_query_conditions(user):
        if not user:
            user = frappe.session.user

        if "QF Technician" in frappe.get_roles(user):
            return f"`tabJob Card`.assigned_technician = '{user}'"

        return None

    def validate(self):

        if self.customer_phone:
            if not self.customer_phone.isdigit() or len(self.customer_phone) != 10:
                frappe.throw("Customer Phone must be exactly 10 digits")

        if self.status in ["In Repair", "Ready for Delivery", "Delivered"]:
            if not self.assigned_technician:
                frappe.throw("Assigned Technician is required when status is In Repair or beyond.")

        parts_total = 0
        for row in self.table_bgvh:
            row.total_price = (row.quantity or 0) * (row.unit_price or 0)
            parts_total += row.total_price

        self.parts_total = parts_total

        if not self.labour_charge:
            self.labour_charge = frappe.db.get_single_value(
                "QuickFix Settings",
                "default_labour_charge"
            ) or 0

        self.final_amount = (self.parts_total or 0) + (self.labour_charge or 0)

    def before_submit(self):

        if self.status != "Ready for Delivery":
            frappe.throw("Job Card can only be submitted when status is 'Ready for Delivery'.")

        for row in self.table_bgvh:
            stock_qty = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

            if stock_qty < (row.quantity or 0):
                frappe.throw(
                    f"Insufficient stock for Part: {row.part}. "
                    f"Available: {stock_qty}, Required: {row.quantity}"
                )

    def on_submit(self):
        self.notify_job_ready()

        for row in self.table_bgvh:
            stock_qty = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

            frappe.db.set_value(
                "Spare Part",
                row.part,
                "stock_qty",
                stock_qty - (row.quantity or 0)
            )

        self.create_service_invoice()

    def create_service_invoice(self):

        if frappe.db.exists("Service Invoice", {"job_card": self.name}):
            return

        parts_total = sum(row.total_price for row in self.table_bgvh)

        invoice = frappe.get_doc({
            "doctype": "Service Invoice",
            "job_card": self.name,
            "customer_name": self.customer_name,
            "invoice_date": nowdate(),
            "labour_charge": self.labour_charge,
            "parts_total": parts_total,
            "total_amount": parts_total + (self.labour_charge or 0),
            "payment_status": "Unpaid"
        })

        invoice.insert(ignore_permissions=True)
        invoice.submit()

        frappe.msgprint(f"Service Invoice {invoice.name} Created Successfully")

    def notify_job_ready(self):

        # Realtime event
        frappe.publish_realtime(
            event="job_ready",
            message={
                "job_card": self.name,
                "customer": self.customer_name,
                "message": f"Job Card {self.name} is Ready"
            },
            user=None
        )

        # Background email job
        frappe.enqueue(
            method=send_job_ready_email,   
            queue="short",
            job_card=self.name,
            customer=self.customer_name
        )

    def on_cancel(self):

        
        self.db_set("status", "Cancelled")

        
        for row in self.table_bgvh:
            stock_qty = frappe.db.get_value(
                "Spare Part",
                row.part,
                "stock_qty"
            ) or 0

            frappe.db.set_value(
                "Spare Part",
                row.part,
                "stock_qty",
                stock_qty + (row.quantity or 0)
            )

        
        invoice_name = frappe.db.get_value(
            "Service Invoice",
            {"job_card": self.name},
            "name"
        )

        if invoice_name:
            invoice_doc = frappe.get_doc("Service Invoice", invoice_name)

            if invoice_doc.docstatus == 1:
                invoice_doc.cancel()

    def on_trash(self):

        if self.status not in ["Cancelled", "Draft"]:
            frappe.throw(
                "You can only delete Job Cards that are in Draft or Cancelled status."
            )


def send_job_ready_email(job_card, customer):

    doc = frappe.get_doc("Job Card", job_card)

    if not doc.customer_email:
        frappe.log_error("Customer Email Missing", f"Job Card: {job_card}")
        return

    frappe.sendmail(
        recipients=[doc.customer_email],
        subject=f"Your Device is Ready - {job_card}",
        message=f"""
Dear {customer},

Your service job ({job_card}) is completed and ready for pickup.

Thank you for choosing us!

Regards,
QuickFix Service Center
""",
        now=False   # send via queue
    )


