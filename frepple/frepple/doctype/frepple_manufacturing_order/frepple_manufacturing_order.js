// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Manufacturing Order', {
	refresh: function(frm) {
		frm.add_custom_button(__('Export to ERPNext'), function() {
			frm.call({
				method:"generate_erp_wo",
				args:{
					doc: frm.doc
				},
				callback:function(r){
					console.log(r.message)
				},
			})
		});
	}
});
