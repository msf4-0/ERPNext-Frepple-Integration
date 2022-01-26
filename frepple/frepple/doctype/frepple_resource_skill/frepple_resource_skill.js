// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt


frappe.ui.form.on('Frepple Resource Skill', {
	setup: function(frm) {
		frm.set_query('resource', function() {
			return {
				filters: [
					['Frepple Resource', 'employee_check', '=', 1],//Only take Human Resource
					// ['Work Order', 'qty', '>','`tabWork Order`.produced_qty'],
					// ['Work Order', 'company', '=', frm.doc.company]
				]
			}
		});
	}
})
