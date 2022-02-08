# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document

from frepple.frepple.doctype.frepple_integration_data_fetching.frepple_integration_data_fetching import so_status_e2f
class FreppleDemand(Document):
	pass

# Sync the status of work order in erpnext with the manufacturing order in frepple
@frappe.whitelist()
def update_frepple_demand_status(doc):
	doc = json.loads(doc)
	if (frappe.get_doc("Frepple Settings").frepple_integration) and doc["docstatus"]:
		erpnext_so = frappe.get_doc("Sales Order",doc["name"]) #ERPNext sales order

		print(erpnext_so)
		sos = frappe.db.sql(
			"""
			SELECT name,so_owner
			FROM `tabFrepple Demand`
			WHERE so_owner = %s
			""",
		erpnext_so.name,as_dict=1)

		for so in sos:
			frappe.db.set_value('Frepple Demand', so.name, 'status',so_status_e2f(erpnext_so.status)) #Update the status
			print(so_status_e2f(erpnext_so.status))

