frappe.listview_settings['Frepple Manufacturing Order'] = {
    onload(listview) {
        // triggers once before the list is loaded
        console.log("loaded", listview);
        listview.page.add_action_item('Create work order in ERPNext', 
            () => 
            listview.call_for_selected_items("frepple.frepple.doctype.frepple_manufacturing_order.frepple_manufacturing_order.generate_erp_wo_bulk")
        );
    }
}