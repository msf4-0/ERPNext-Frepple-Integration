// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Location', {
	setup: function(frm) {
		frm.set_query('location_owner', function() {
			return {
				filters: [
					['Frepple Location', 'location_owner', '=', ''],
					// ['Work Order', 'qty', '>','`tabWork Order`.produced_qty'],
					// ['Work Order', 'company', '=', frm.doc.company]
				]
			}
		});
	}
});
