frappe.ui.form.on("Bin",{ 
    
    refresh: function(frm) {
        frappe.call({ // call check_duplicate_wo to remove any work order that ady exist to prevent duplicate production plan for the same wo
            method:"frepple.frepple.doctype.frepple_buffer.frepple_buffer.update_frepple_buffer",
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