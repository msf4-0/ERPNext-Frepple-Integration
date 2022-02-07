// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Purchase Order', {
	// after_save:function(frm){
	// 	frm.call({
	// 		method:"generate_erp_po",
	// 		args:{
	// 			doc: frm.doc
	// 		},
	// 		callback:function(r){
	// 			console.log(r.message)
	// 		},
	// 	})
	// },

	refresh: function(frm) {
		frm.add_custom_button(__('Export to ERPNext'), function() {
			frm.call({
				method:"generate_erp_po",
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
