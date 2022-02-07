// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Run Plan', {
	constraint:function(frm){
		if (frm.doc.constraint){
			frm.set_value("unconstraint",0);
			frm.refresh_field('unconstraint');
		}
		else{
			frm.set_value("unconstraint",2);
			frm.refresh_field('unconstraint');
		}
	},
	unconstraint:function(frm){
		if (frm.doc.unconstraint){
			frm.set_value("constraint",0);
			frm.refresh_field('constraint');
		}
		else{
			frm.set_value("constraint",1);
			frm.refresh_field('constraint');
		}
	},

	run_plan:function(frm){
		frm.call({
			method:"run_plan",
			args:{
				doc: frm.doc
			},
			callback:function(r){
				console.log(r.message)
			},
		})
	},

	generate_result:function(frm){
		frm.call({
			method:"generate_result",
			args:{
				doc: frm.doc
			},
			callback:function(r){
				console.log(r.message)
			},
		})
	},
	
});
