# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json

from frappe.model.document import Document

class FrepplePurchaseOrder(Document):
	pass


@frappe.whitelist()
def generate_erp_po(doc):
	doc = json.loads(doc)
	doc = frappe.get_doc("Frepple Purchase Order",doc["name"])
	# item = frappe.db.get_value('BOM', doc.operation, 'item') #get item in such a way because frepple MO does not give us the item name if followed our algorithm
	
	if not doc.erpnext_po:
		new_doc = frappe.new_doc("Purchase Order")
		new_doc.status = po_status_f2e(doc.status)
		new_doc.supplier = doc.supplier
		new_doc.transaction_date = doc.ordering_date  
		new_doc.schedule_date = doc.receive_date
		row = new_doc.append("items",{})
		row.item_code = doc.item
		row.qty = doc.quantity 
		new_doc.insert()

		frappe.db.set_value('Frepple Purchase Order', doc.name, 'erpnext_po', new_doc.name)

# CHeck the erpnext purchase order status and get its correspond frepple purchase status
# Frepple -> ERPNext
def po_status_f2e(status):
	switcher={
		"proposed":'Draft',
		# "approved":'',
		"confirmed":'To Deliver and Bill',
		"closed":'Closed',
		"completed":'Completed',

		}
	return switcher.get(status,"Draft")

