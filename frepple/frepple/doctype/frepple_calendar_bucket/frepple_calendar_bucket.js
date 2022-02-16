// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Calendar Bucket', {
	after_save:function(frm){
		frm.call({
			method:"add_to_calendar",
			doc: frm.doc,
			// method:"make_request",
			callback:function(r){
			}
		});
	},

	validate:function(frm){
		frm.call({
			method:"check_priority",
			doc: frm.doc,
			// method:"make_request",
			callback:function(r){
				var duplicate = r.message
				if (duplicate){
					frappe.validated = false
					frappe.msgprint({
						title: __('Notice'),
						indicator: 'red',
						message: __('Priority is duplicate. Please modify it.')
					});
				}
			}
		});
	}
});
