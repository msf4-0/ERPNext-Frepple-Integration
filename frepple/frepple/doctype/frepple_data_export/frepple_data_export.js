// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Data Export', {
	export_data_to_frepple(frm){
		frm.call({
			method:"export_data",
			args:{
				doc: frm.doc
			},
			callback:function(r){
				console.log(r.message)
			},
		})
	},
	
	select_all(frm){
		var fields = frm.fields_dict;
		for (const field in fields)
		{
			if(fields[field].df.fieldtype=="Check" && fields[field].df.read_only == 0)
			{
				frm.set_value(fields[field].df.fieldname,1);
			}
		}
	},
	deselect_all(frm){
		var fields = frm.fields_dict;
		for (const field in fields)
		{
			if(fields[field].df.fieldtype=="Check"  && fields[field].df.read_only == 0)
			{
				frm.set_value(fields[field].df.fieldname,0);
			}
		}
	}
});
