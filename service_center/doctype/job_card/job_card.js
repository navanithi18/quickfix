frappe.ui.form.on('Job Card', {

    setup: function(frm) {

        frm.set_query("assigned_technician", function() {
            return {
                filters: {
                    status: "Active",
                    specialization: frm.doc.device_type
                }
            };
        });

    },

    onload: function(frm) {

        frappe.realtime.on("job_ready", function(data){
            frappe.show_alert({
                message: "Job is ready!",
                indicator: "green"
            });
        });

    },

    refresh: function(frm) {

        // Dashboard indicators
        if(frm.doc.status == "Pending"){
            frm.dashboard.add_indicator("Pending", "orange");
        }

        if(frm.doc.status == "In Repair"){
            frm.dashboard.add_indicator("In Repair", "blue");
        }

        if(frm.doc.status == "Ready for Delivery"){
            frm.dashboard.add_indicator("Ready for Delivery", "green");
        }

        if(frm.doc.status == "Completed"){
            frm.dashboard.add_indicator("Completed", "gray");
        }

        // Mark as Delivered
        if(frm.doc.status == "Ready for Delivery" && frm.doc.docstatus == 1){

            frm.add_custom_button("Mark as Delivered", function(){

                frappe.call({
                    method: "quickfix.api.mark_as_delivered",
                    args: {
                        job_card: frm.doc.name
                    },
                    callback: function(){
                        frappe.show_alert("Marked as Delivered");
                        frm.reload_doc();
                    }
                });

            });

        }

        // Reject Job
        if (frm.doc.docstatus == 1 && frm.doc.status == "Ready for Delivery") {

            frm.add_custom_button("Reject Job", function(){

                let d = new frappe.ui.Dialog({
                    title: "Reject Job",
                    fields: [
                        {
                            label: "Rejection Reason",
                            fieldname: "reason",
                            fieldtype: "Small Text",
                            reqd: 1
                        }
                    ],
                    primary_action_label: "Submit",

                    primary_action(values){

                        frappe.call({
                            method: "quickfix.api.reject_job",
                            args: {
                                job_card: frm.doc.name,
                                reason: values.reason
                            },
                            callback: function(){
                                frappe.msgprint("Job Rejected");
                                d.hide();
                                frm.reload_doc();
                            }
                        });

                    }
                });

                d.show();

            });

        }

        // Transfer Technician
        frm.add_custom_button("Transfer Technician", function(){

            frappe.prompt(
                [
                    {
                        label: "New Technician",
                        fieldname: "technician",
                        fieldtype: "Link",
                        options: "Technician",
                        reqd: 1
                    }
                ],

                function(values){

                    frappe.confirm(
                        "Are you sure you want to transfer technician?",

                        function(){

                            frappe.call({
                                method: "quickfix.api.transfer_technician",
                                args: {
                                    job_card: frm.doc.name,
                                    technician: values.technician
                                },
                                callback: function(){

                                    frm.set_value("assigned_technician", values.technician);
                                    frm.trigger("assigned_technician");

                                    frappe.show_alert("Technician Transferred");

                                }
                            });

                        }
                    );

                },

                "Transfer Technician",
                "Transfer"
            );

        });

        // Shop name in header
        if(frappe.boot.quickfix_shop_name){
            frm.page.set_title(
                frm.doc.name + " - " + frappe.boot.quickfix_shop_name
            );
        }

    },

    assigned_technician: function(frm){

        if(!frm.doc.assigned_technician) return;

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Technician",
                fieldname: "specialization",
                filters: {
                    name: frm.doc.assigned_technician
                }
            },
            callback: function(r){

                let spec = r.message.specialization;

                if(spec != frm.doc.device_type){
                    frappe.msgprint(
                        "Warning: Technician specialization does not match device type"
                    );
                }

            }
        });

    }

});

frappe.ui.form.on("Part", {

    quantity: function(frm, cdt, cdn){

        let row = locals[cdt][cdn];

        if(row.quantity && row.unit_price){

            let total = row.quantity * row.unit_price;

            frappe.model.set_value(
                cdt,
                cdn,
                "total_price",
                total
            );
        }

    }

});