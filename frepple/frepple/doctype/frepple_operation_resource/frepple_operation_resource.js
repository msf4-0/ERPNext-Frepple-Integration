// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Operation Resource', {
	// refresh: function(frm) {

	// }
	employee_check:function(frm){
		if(frm.doc.employee_check){
			frm.call({
				method:"add_default_employee",
				callback:function(r){
					console.log(r.message)
					frm.set_value('resource',r.message );
				},
			})
			frm.toggle_enable(['resource'], false);
		}
		else{
			frm.toggle_enable(['resource'], true);
			frm.set_value('resource',"" );
			frm.set_value('skill',"" );
		}

	}
});
