# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _

from frappe.model.document import Document

class FrepplePurchaseOrder(Document):
	pass

@frappe.whitelist()
def generate_erp_po_bulk(names):
	names = json.loads(names)
	for name in names:
		po = frappe.get_doc("Frepple Purchase Order", name)

		if not po.erpnext_po:
			new_doc = frappe.new_doc("Purchase Order")
			new_doc.status = po_status_f2e(po.status)
			new_doc.supplier = po.supplier
			new_doc.transaction_date = po.ordering_date  
			new_doc.schedule_date = po.receive_date
			row = new_doc.append("items",{})
			row.item_code = po.item
			row.qty = po.quantity 
			new_doc.insert()

			frappe.db.set_value('Frepple Purchase Order', po.name, 'erpnext_po', new_doc.name)
			

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
		frappe.msgprint(_("Purchase order exported successfully."))

	else:
		frappe.msgprint(_("Duplicate purchase order. Purchase order is not created"))

# Sync the status of purchase order in erpnext with the purchase order in frepple
@frappe.whitelist()
def update_frepple_po_status(doc):
	doc = json.loads(doc)
	if (frappe.get_doc("Frepple Settings").frepple_integration) and doc["docstatus"]:
		erpnext_po = frappe.get_doc("Purchase Order",doc["name"]) #ERPNext purchase order

		pos = frappe.db.sql(
			"""
			SELECT name,erpnext_po
			FROM `tabFrepple Purchase Order`
			WHERE erpnext_po = %s
			""",
		erpnext_po.name,as_dict=1)

		for po in pos:
			# mo = frappe.db.get_list('Frepple Manufacturing Order', filters={
			# 	'erpnext_wo': [wo.name]	
			# }) # Get the frepple manufacturing order with owner work order match

			# print(mo[0])
			frappe.db.set_value('Frepple Purchase Order', po.name, 'status',po_status_e2f(erpnext_po.status)) #Update the status
			print(po_status_e2f(erpnext_po.status))

# CHeck the erpnext purchase order status and get its correspond frepple purchase status
# ERPNExt -> Frepple
def po_status_e2f(status):
	switcher={
		"Draft":'proposed',
		"On Hold":'approved',
		"To Receive and Bill":'confirmed',
		"To Bill":'confirmed',
		"To Deliver":'confirmed',
		"Completed":'completed',
		"Cancelled":'canceled',
		"Closed":'closed',
		"Delivered":'closed'
		}
	return switcher.get(status,"proposed")

	'ERPNext'				'Frepple'
	# Draft					proposed
	# On Hold				approved
	# To Deliver and Bill	confirmed
	# To Bill				closed
	# To Deliver			completed
	# Completed
	# Cancelled
	# Closed
	# Delivered

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
	return switcher.get(status,"inquiry")
	switcher={
		"proposed":'Draft',
		# "approved":'',
		"confirmed":'To Deliver and Bill',
		"closed":'Closed',
		"completed":'Completed',

	}
	return switcher.get(status,"Draft")

