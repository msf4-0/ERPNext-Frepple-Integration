frappe.ui.form.on("Purchase Order",{ 
    
    refresh: function(frm) {
        frappe.call({ // call check_duplicate_wo to remove any work order that ady exist to prevent duplicate production plan for the same wo
            method:"frepple.frepple.doctype.frepple_purchase_order.frepple_purchase_order.update_frepple_po_status",
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