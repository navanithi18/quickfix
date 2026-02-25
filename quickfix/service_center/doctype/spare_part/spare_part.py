# Copyright (c) 2026, navanithi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SparePart(Document):
    def validate(self):
       
        if self.selling_price <= self.unit_cost:
            frappe.throw("Selling Price must be greater than Unit Cost")