frappe.query_reports["Technician Performance Report"] = {

    formatter: function(value, row, column, data, default_formatter) {

        value = default_formatter(value, row, column, data);

        if (column.fieldname == "completion_rate") {

            if (data.completion_rate < 70) {
                value = "<span style='color:red'>" + value + "</span>";
            }

            if (data.completion_rate >= 90) {
                value = "<span style='color:green'>" + value + "</span>";
            }

        }

        return value;
    }

};