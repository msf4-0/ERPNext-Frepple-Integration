// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Integration Data Fetching', {
	// refresh: function(frm) {

	// }
	get_data_for_frepple(frm){
		frm.call({
			method:"fetch_data",
			args:{
				doc: frm.doc
			}
		})
	},
	select_all(frm){
		var fields = frm.fields_dict;
		for (const field in fields)
		{
			if(fields[field].df.fieldtype=="Check")
			{
				frm.set_value(fields[field].df.fieldname,1);
			}
		}
	},
	deselect_all(frm){
		var fields = frm.fields_dict;
		for (const field in fields)
		{
			if(fields[field].df.fieldtype=="Check")
			{
				frm.set_value(fields[field].df.fieldname,0);
			}
		}
	}
});
