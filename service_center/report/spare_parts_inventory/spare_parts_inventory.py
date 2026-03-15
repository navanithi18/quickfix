import frappe

def execute(filters=None):

    columns = [
        {"label": "Part Name", "fieldname": "part_name", "fieldtype": "Data", "width": 150},
        {"label": "Part Code", "fieldname": "part_code", "fieldtype": "Data", "width": 120},
        {"label": "Device Type", "fieldname": "device_type", "fieldtype": "Link", "options": "Device Type", "width": 150},
        {"label": "Stock Qty", "fieldname": "stock_qty", "fieldtype": "Float", "width": 100},
        {"label": "Reorder Level", "fieldname": "reorder_level", "fieldtype": "Float", "width": 120},
        {"label": "Unit Cost", "fieldname": "unit_cost", "fieldtype": "Currency", "width": 120},
        {"label": "Selling Price", "fieldname": "selling_price", "fieldtype": "Currency", "width": 120},
        {"label": "Margin %", "fieldname": "margin", "fieldtype": "Float", "width": 100},
        {"label": "Total Value", "fieldname": "total_value", "fieldtype": "Currency", "width": 150},
    ]

    parts = frappe.get_list(
        "Spare Part",
        fields=[
            "part_name",
            "part_code",
            "device_type",
            "stock_qty",
            "reorder_level",
            "unit_cost",
            "selling_price"
        ]
    )

    data = []
    total_stock = 0
    total_value = 0
    below_reorder = 0

    for p in parts:

        stock_qty = p.stock_qty or 0
        reorder_level = p.reorder_level or 0

        margin = 0
        if p.unit_cost:
            margin = ((p.selling_price - p.unit_cost) / p.unit_cost) * 100

        value = stock_qty * (p.unit_cost or 0)

        if stock_qty <= reorder_level:
            below_reorder += 1

        total_stock += stock_qty
        total_value += value

        data.append({
            "part_name": p.part_name,
            "part_code": p.part_code,
            "device_type": p.device_type,
            "stock_qty": stock_qty,
            "reorder_level": reorder_level,
            "unit_cost": round(p.unit_cost or 0, 2),
            "selling_price": round(p.selling_price or 0, 2),
            "margin": round(margin, 2),
            "total_value": round(value, 2)
        })

    data.append({
        "part_name": "TOTAL",
        "stock_qty": total_stock,
        "total_value": total_value
    })

    summary = [
        {"label": "Total Parts", "value": len(parts), "indicator": "Blue"},
        {"label": "Below Reorder", "value": below_reorder, "indicator": "Red"},
        {"label": "Total Inventory Value", "value": total_value, "indicator": "Green"}
    ]

    return columns, data, None, None, summary