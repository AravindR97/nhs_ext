
frappe.ui.form.on("Sales Order", {

    validate: function(frm) {

        let below_msp = 0;

        (frm.doc.items || []).forEach(function(row) {

            if (row.rate && row.price_list_rate && row.rate < row.price_list_rate) {
                below_msp = 1;
            }

        });

        frm.set_value("custom_below_rate", below_msp);

    },
    onload: function(frm) {
        frappe.db.get_single_value("Selling Settings", "custom_enable_the_price_list_validation")
        .then((value) => {
            if (value) {
                frm.set_value("custom_enable_from_settings", 1);
            } else {
                frm.set_value("custom_enable_from_settings", 0);
            }
            frm.refresh_field("custom_enable_from_settings");
        });
    }

});