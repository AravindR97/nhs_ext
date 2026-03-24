import frappe





def validate_msp_price(doc, method):
    try:
        enable_validation = frappe.db.get_single_value(
            "Selling Settings",
            "custom_enable_the_price_list_validation"
        )
    except Exception:
        enable_validation = 0  
    if not enable_validation:
        doc.custom_below_rate = 0
        return
    doc.custom_below_rate = 0
    below_items = []
    for item in getattr(doc, "items", []):
        if not item.item_code:
            continue

        price_list_rate = frappe.db.get_value(
            "Item Price",
            {
                "item_code": item.item_code,
                "price_list": getattr(doc, "selling_price_list", None)
            },
            "price_list_rate"
        )

        if price_list_rate and item.rate < price_list_rate:
            below_items.append((item.idx, item.item_code, price_list_rate))

    if below_items:
        doc.custom_below_rate = 1

        messages = "\n".join(
            [f"Row {idx}: Item {code} below MSP ({rate})"
             for idx, code, rate in below_items]
        )

        frappe.msgprint(
            f"Approval required for below-MSP items:\n{messages}"
        )