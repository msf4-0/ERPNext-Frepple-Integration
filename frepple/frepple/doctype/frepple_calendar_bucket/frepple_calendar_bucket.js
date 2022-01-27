// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Calendar Bucket', {
	after_save:function(frm){
		frm.call({
			method:"add_to_calendar",
			doc: frm.doc,
			// method:"make_request",
			callback:function(r){
				console.log(r.message)
			}
		});

	}
});
