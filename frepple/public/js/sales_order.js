frappe.ui.form.on("Sales Order",{ 
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
        
        //By default add 4 days to the delivery date
        if (frm.docstatus !== 1){
            var date = frappe.datetime.add_days(frm.doc.transaction_date, 4); 
            frm.set_value("delivery_date", date); 
        }
    }
});
