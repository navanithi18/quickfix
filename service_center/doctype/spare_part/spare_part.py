import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):

    def validate(self):
        if self.selling_price <= self.unit_cost:
            frappe.throw("Selling Price must be greater than Unit Cost")

    def autoname(self):
        if not self.part_code:
            frappe.throw("Part Code is required")

        self.part_code = self.part_code.upper()

        self.name = make_autoname("PART-.YYYY.-.####")