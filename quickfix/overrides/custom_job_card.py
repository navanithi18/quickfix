# Copyright (c) 2026, navanithi
# For license information, please see license.txt

import frappe
from quickfix.service_center.doctype.job_card.job_card import JobCard


"""
Method Resolution Order (MRO):

MRO means the order in which Python searches for methods when a class
inherits from another class.

Here CustomJobCard extends JobCard. When a method like validate() is called,
Python first checks CustomJobCard, then JobCard, then the parent classes.

We call super().validate() to make sure the original validation logic
written in JobCard still runs before our custom logic.

Calling super() is very important because if we skip it, the original
validations of JobCard will not execute and it may break the normal
working of the system.
"""


"""
When to use override_doctype_class vs doc_events:

override_doctype_class is used when we want to change or extend the main
behavior of a DocType by creating a new class that inherits the original one.

doc_events is used when we only want to trigger some extra actions
during events like validate, before_save, on_submit etc.

.

If we only wanted to log something or send a small notification
when the document is saved, then doc_events would be enough.
"""


class CustomJobCard(JobCard):

    def validate(self):
        super().validate()
        self._check_urgent_unassigned()

    def _check_urgent_unassigned(self):

        if self.priority == "Urgent" and not self.assigned_technician:

            settings = frappe.get_single("QuickFix Settings")

            frappe.enqueue(
                "quickfix.utils.send_urgent_alert",
                job_card=self.name,
                manager=settings.manager_email
            )