frappe.listview_settings['Job Card'] = {

    add_fields: ["status", "final_amount", "priority"],
    has_indicator_for_draft: true,
    get_indicator: function(doc) {

        if (doc.status === "Pending Diagnosis") {
            return ["Pending Diagnosis", "orange", "status,=,Pending Diagnosis"];
        }

        if (doc.status === "In Repair") {
            return ["In Repair", "blue", "status,=,In Repair"];
        }

        if (doc.status === "Ready for Delivery") {
            return ["Ready", "green", "status,=,Ready for Delivery"];
        }

        if (doc.status === "Cancelled") {
            return ["Cancelled", "red", "status,=,Cancelled"];
        }

    },

    formatters: {

        final_amount(value) {
            if (!value) return "₹0";
            return "₹ " + value;
        }

    },

    button: {

        show: function(doc) {
            return doc.status === "In Repair";
        },

        get_label: function() {
            return "Complete";
        },

        action: function(doc) {

            frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "Job Card",
                    name: doc.name,
                    fieldname: "status",
                    value: "Ready for Delivery"
                },
                callback: function() {
                    frappe.show_alert("Job Completed");
                    frappe.listview.refresh();
                }
            });

        }

    }

};