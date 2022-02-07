// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Custom Page Settings', {
	refresh:function(frm){
		
		frm.call({
			method:"get_secret_key",
			callback:function(r){
				frm.set_value('secret_key',r.message );
			},
		})

		if (frm.secret_key){
			frm.toggle_enable(['secret_key'], true);
		}
		else{
			frm.toggle_enable(['secret_key'], false);
		}
	}
});
