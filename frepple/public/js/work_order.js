frappe.ui.form.on("Work Order",{ 
    
    refresh: function(frm) {
        frappe.call({ // call check_duplicate_wo to remove any work order that ady exist to prevent duplicate production plan for the same wo
            method:"frepple.frepple.doctype.frepple_manufacturing_order.frepple_manufacturing_order.update_frepple_mo_status",
            args: {
                //Argument we defined in method : argument to pass to
                doc:frm.doc,
            },
            callback: function(r) {
                console.log(r.message)
            }
        })
    },
    
})