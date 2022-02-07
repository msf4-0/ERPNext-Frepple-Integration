frappe.listview_settings['Frepple Purchase Order'] = {
    onload(listview) {
        // triggers once before the list is loaded
        console.log("loaded", listview);
        listview.page.add_action_item('Create purchase order in ERPNext', 
            () => 
            listview.call_for_selected_items("frepple.frepple.doctype.frepple_purchase_order.frepple_purchase_order.generate_erp_po_bulk")
        );
    }
}