frappe.query_reports["Spare Parts Inventory"] = {
	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (!data || data.part_name === "TOTAL") {
			return value;
		}

		const stockQty = flt(data.stock_qty);
		const reorderLevel = flt(data.reorder_level);

		if (stockQty <= reorderLevel) {
			value = "<span style='background-color:#ffcccc'>" + value + "</span>";
		}

		return value;
	}
};
