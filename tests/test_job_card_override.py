import frappe
from frappe.tests.utils import FrappeTestCase


class TestJobCardOverride(FrappeTestCase):

    def test_super_validate_called(self):

        job = frappe.get_doc({
            "doctype": "Job Card",
            "customer_name": "Test Customer",
            "customer_phone": "9999999999",
            "device_type": "Laptop",
            "problem_description": "Screen issue"
        })

        job.insert()

        # If validate() from base class does not run,
        # the naming series or validations may fail
        self.assertTrue(job.name.startswith("JC-"))