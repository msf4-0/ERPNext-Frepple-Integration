// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Operation', {
	setup: function(frm) {
		frm.set_query('operation_owner', function() {
			return {
				filters: [
					['Frepple Operation', 'type', '=', 'routing'],
					// ['Work Order', 'qty', '>','`tabWork Order`.produced_qty'],
					// ['Work Order', 'company', '=', frm.doc.company]
				]
			}
		});
	}
})

