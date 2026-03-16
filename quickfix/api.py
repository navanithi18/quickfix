import frappe

@frappe.whitelist()
def share_job_card(job_card_name, user_email):
    if not frappe.db.exists("Job Card", job_card_name):
        frappe.throw("Job Card not found")

    if not frappe.db.exists("User", user_email):
        frappe.throw("User not found")

    frappe.share.add(
        doctype="Job Card",
        name=job_card_name,
        user=user_email,
        read=1,
        write=0,
        share=0,
        submit=0
    )

    return f"Job Card {job_card_name} shared with {user_email}"


@frappe.whitelist()
def manager_only_action():
    
    frappe.only_for("QF Manager")

    return "Welcome QF Manager! You are authorized."

    


@frappe.whitelist()
def get_job_cards_safe():

    user = frappe.session.user
    roles = frappe.get_roles(user)

    # Permission-aware query
    job_cards = frappe.get_list(
        "Job Card",
        fields=[
            "name",
            "customer_name",
            "device_model",
            "issue_description",
            "payment_status",
            "customer_phone",
            "customer_email"
        ]
    )

    # Strip sensitive fields for non-Managers
    if "Manager" not in roles and "System Manager" not in roles:
        for jc in job_cards:
            jc.pop("customer_phone", None)
            jc.pop("customer_email", None)

    return job_cards


    #
@frappe.whitelist()
def custom_get_count(doctype, filters=None, debug=False, cache=False):
    # Log the request to Audit Log
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": doctype,
        "action": "count_queried",
        "user": frappe.session.user
    }).insert(ignore_permissions=True)
    
    # Call original behaviour
    from frappe.client import get_count
    return get_count(doctype, filters, debug, cache)