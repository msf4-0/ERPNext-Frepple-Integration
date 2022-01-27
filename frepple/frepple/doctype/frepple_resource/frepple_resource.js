// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Resource', {
	// refresh: function(frm) {
	validate: function(frm) {
		if(frm.doc.workstation_check){
			frm.set_value('name1', frm.doc.workstation);
			frm.refresh_field('name1');
		}
		if(frm.doc.employee_check){
			frm.set_value('name1', frm.doc.employee);
			frm.refresh_field('name1');
		}
	},
	employee_check:function(frm){
		if (employee_check){
			frm.set_value('resource_owner','Operator')
		}
	},

	workstation_check:function(frm){
		if (workstation_check){
			frm.set_value('resource_owner','Workstation')
		}
	}
	
	// }
});
