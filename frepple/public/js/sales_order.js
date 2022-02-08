frappe.ui.form.on("Sales Order",{ 

    // refresh:function(frm){
    //     frappe.call({ // call check_duplicate_wo to remove any work order that ady exist to prevent duplicate production plan for the same wo
    //         method:"frepple.frepple.doctype.frepple_demand.frepple_demand.update_frepple_demand_status",
    //         args: {
    //             //Argument we defined in method : argument to pass to
    //             doc:frm.doc,
    //         },
    //         callback: function(r) {
    //             console.log(r.message)
    //         }
    //     })
    // },


    // "transaction_date":function(frm) { 
    //     var p = frm.doc; 
    //     var date = frappe.datetime.get_today();
    //     if (frm.doc.transaction_date < date) { 
    //         frappe.model.set_value(p.doctype, p.name, "transaction_date", frappe.datetime.get_today()); 
    //         //frappe.msgprint("Please do not select the past date");
    //         frappe.msgprint({
    //             title: __('Warning'),
    //             indicator: 'red',
    //             message: __('Please do not select the past day!')
    //         });
    //     } 
    // },
    // "delivery_date":function(frm,cdt,cdn) { 
    //     var p = frm.doc; 
    //     var date = frappe.datetime.add_days(frm.doc.transaction_date, 4); 
    
    //     if (frm.doc.delivery_date < date) { 
    //         frappe.model.set_value(p.doctype, p.name, "delivery_date", date); 
    //         //alert("Please select another date");
    //         frappe.msgprint({
    //             title: __('Warning'),
    //             indicator: 'red',
    //             message: __('Delivery date should be at least one day later than the sales order opening date!')
    //         }); 
    //     }
    //     //trying to update the item delivery date after i update the main delivery date.
    //     var d = locals[cdt][cdn];
	//     //d.delivery_date = frm.doc.delivery_date;
	//     frm.doc.items.forEach(function(d) {
	//         if (d.delivery_date !== frm.doc.delivery_date){
	// 	    frappe.model.set_value(d.doctype, d.name, 'delivery_date', frm.doc.delivery_date);
	//         }
	//     });
    // },    

    refresh:function(frm){
        frappe.call({ // call check_duplicate_wo to remove any work order that ady exist to prevent duplicate production plan for the same wo
            method:"frepple.frepple.doctype.frepple_demand.frepple_demand.update_frepple_demand_status",
            args: {
                //Argument we defined in method : argument to pass to
                doc:frm.doc,
            },
            callback: function(r) {
                console.log(r.message)
            }
        })

        if (frm.docstatus !== 1){
            var date = frappe.datetime.add_days(frm.doc.transaction_date, 4); 
            frm.set_value("delivery_date", date); 
        }
    }
});

// // SOlve the problem where the delivery date depend on the most recent update in the items table. This
// // code can update all item date based on one item delivery date, meanwhile, update the main delivery date.
// frappe.ui.form.on('Sales Order Item', {
// 	item_code:function(frm, cdt, cdn){
// 		var d = locals[cdt][cdn];
// 		 // another === condition is to update the all item date if main delivery date change after add new item
// 		if (d.delivery_date !== frm.doc.delivery_date || d.delivery_date === frm.doc.delivery_date){
// 		    frm.doc.delivery_date = d.delivery_date;
// 		    frm.doc.items.forEach(function(d) {
// 			    frappe.model.set_value(d.doctype, d.name, 'delivery_date', frm.doc.delivery_date);
// 		    });
// 		    frm.refresh_field('delivery_date');
// 	    }
// 	},
// 	delivery_date:function(frm, cdt, cdn){
// 		var d = locals[cdt][cdn];
// 		 // another === condition is to update the all item date if main delivery date change after add new item
// 		if (d.delivery_date !== frm.doc.delivery_date || d.delivery_date === frm.doc.delivery_date){
// 		    frm.doc.delivery_date = d.delivery_date;
// 		    frm.doc.items.forEach(function(d) {
// 			    frappe.model.set_value(d.doctype, d.name, 'delivery_date', frm.doc.delivery_date);
// 		    });
// 		    frm.refresh_field('delivery_date');
// 	    }
// 	}
// });