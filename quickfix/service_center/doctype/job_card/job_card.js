frappe.realtime.on("job_ready", function(data) {
    frappe.show_alert({
        message: data.message,
        indicator: "green"
    });
});