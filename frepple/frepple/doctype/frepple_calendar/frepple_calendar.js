// Copyright (c) 2022, Drayang Chua and contributors
// For license information, please see license.txt

frappe.ui.form.on('Frepple Calendar', {
	refresh: function(frm) {
		frm.add_custom_button(__('Frepple Resource'), function() {
			erpnext.utils.map_current_doc({
				method: "frepple.frepple.doctype.frepple_calendar.frepple_calendar.fetch_available_2_resource",
				source_doctype: "Frepple Resource",
				target: frm,
				date_field: "creation",
				setters: {
				},
				get_query_filters: {
					// docstatus: 1
				}
			})
		}, __("Fetch items to"));
	}
});

frappe.ui.form.on('Frepple Calendar', {
	refresh: function(frm) {
		frm.add_custom_button(__('Frepple Location'), function() {
			erpnext.utils.map_current_doc({
				method: "frepple.frepple.doctype.frepple_calendar.frepple_calendar.fetch_available_2_location",
				source_doctype: "Frepple Location",
				target: frm,
				date_field: "creation",
				setters: {
				},
				get_query_filters: {
					// docstatus: 1
				}
			})
		}, __("Fetch items to"));
	}
});