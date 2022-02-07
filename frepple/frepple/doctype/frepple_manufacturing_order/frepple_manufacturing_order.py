# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json

from frappe.model.document import Document

class FreppleManufacturingOrder(Document):
	pass

@frappe.whitelist()
def generate_erp_wo(doc):
	doc = json.loads(doc)
	doc = frappe.get_doc("Frepple Manufacturing Order",doc["name"])
	item = frappe.db.get_value('BOM', doc.operation, 'item') #get item in such a way because frepple MO does not give us the item name if followed our algorithm
	if not doc.erpnext_wo:
		new_doc = frappe.new_doc("Work Order")
		new_doc.status = mo_status_f2e(doc.status)
		new_doc.production_item = item
		new_doc.bom_no = doc.operation  
		new_doc.qty = doc.quantity
		new_doc.planned_start_date = doc.start_date
		new_doc.planned_end_date = doc.end_date
		new_doc.insert()
		print(new_doc.name)
		doc.erpnext_wo = new_doc.name
		print(doc.erpnext_wo)

		frappe.db.set_value('Frepple Manufacturing Order', doc.name, 'erpnext_wo', new_doc.name)

# CHeck the erpnext work order status and get its correspond frepple manufacturing order status
# Frepple -> ERPNExt
def mo_status_f2e(status):
	switcher={
		"proposed":'Draft',
		"confirmed":'Submitted',
		"approved":'Not Started',
		"completed":'Completed',
		"cancelled":'Cancelled',
	}
	return switcher.get(status,"proposed") #default is "proposed" status