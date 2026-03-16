console.log("QuickFix Job Card JS Loaded");

frappe.ui.form.on('Job Card', {
    refresh: function(frm) {
        if (frappe.session.user != "Administrator") {
            frm.set_df_property("customer_phone", "hidden", 1);
        }
    }
});
