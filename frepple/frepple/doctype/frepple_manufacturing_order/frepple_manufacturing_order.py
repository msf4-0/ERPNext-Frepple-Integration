# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.document import Document

class FreppleManufacturingOrder(Document):
	pass

'''
Work order in ERPNext = wo
Manufacturing order in Frepple = mo
'''

@frappe.whitelist()
def generate_erp_wo_bulk(names):
	names = json.loads(names)
	for name in names:
		mo = frappe.get_doc("Frepple Manufacturing Order", name)
		item = frappe.db.get_value('BOM', mo.operation, 'item') #get item in such a way because frepple MO does not give us the item name if followed our algorithm
		
		demand = frappe.get_doc("Frepple Demand", mo.demand)
		so_link = demand.so_owner #sales order that it linked to

		if mo.erpnext_wo: #if the manufacturing order already linked to a work order and the work order ady cancelled.
			wo = frappe.get_doc("Work Order",mo.erpnext_wo)
			if wo.status == "Cancelled": 
				new_doc = frappe.new_doc("Work Order")
				new_doc.status = mo_status_f2e(mo.status)
				new_doc.production_item = item
				new_doc.bom_no = mo.operation  
				new_doc.qty = mo.quantity
				new_doc.planned_start_date = mo.start_date
				new_doc.planned_end_date = mo.end_date
				new_doc.sales_order = so_link
				new_doc.insert()
				print(new_doc.name)
				mo.erpnext_wo = new_doc.name
				frappe.db.set_value('Frepple Manufacturing Order', mo.name, 'erpnext_wo', new_doc.name)
				
		if not mo.erpnext_wo: #if not work order is created based on this manufacturing order yet
			new_doc = frappe.new_doc("Work Order")
			new_doc.status = mo_status_f2e(mo.status)
			new_doc.production_item = item
			new_doc.bom_no = mo.operation  
			new_doc.qty = mo.quantity
			new_doc.planned_start_date = mo.start_date
			new_doc.planned_end_date = mo.end_date
			new_doc.sales_order = so_link
			new_doc.insert()
			print(new_doc.name)
			mo.erpnext_wo = new_doc.name
			frappe.db.set_value('Frepple Manufacturing Order', mo.name, 'erpnext_wo', new_doc.name)

@frappe.whitelist()
def generate_erp_wo(doc):
	doc = json.loads(doc)
	mo = frappe.get_doc("Frepple Manufacturing Order",doc["name"])
	item = frappe.db.get_value('BOM', mo.operation, 'item') #get item in such a way because frepple MO does not give us the item name if followed our algorithm
	
	demand = frappe.get_doc("Frepple Demand", mo.demand)
	so_link = demand.so_owner #sales order that it linked to

	if mo.erpnext_wo:
		wo = frappe.get_doc("Work Order",mo.erpnext_wo)
		if wo.status == "Cancelled":
			new_doc = frappe.new_doc("Work Order")
			new_doc.status = mo_status_f2e(mo.status)
			new_doc.production_item = item
			new_doc.bom_no = mo.operation  
			new_doc.qty = mo.quantity
			new_doc.planned_start_date = mo.start_date
			new_doc.planned_end_date = mo.end_date
			new_doc.sales_order = so_link
			new_doc.insert()
			mo.erpnext_wo = new_doc.name
			frappe.db.set_value('Frepple Manufacturing Order', mo.name, 'erpnext_wo', new_doc.name)
			frappe.msgprint(_("New work order is exported successfully."))

			return 
	
	if not mo.erpnext_wo:
		new_doc = frappe.new_doc("Work Order")
		new_doc.status = mo_status_f2e(mo.status)
		new_doc.production_item = item
		new_doc.bom_no = mo.operation  
		new_doc.qty = mo.quantity
		new_doc.planned_start_date = mo.start_date
		new_doc.planned_end_date = mo.end_date
		new_doc.sales_order = so_link
		new_doc.insert()
		print(new_doc.name)
		mo.erpnext_wo = new_doc.name

		frappe.db.set_value('Frepple Manufacturing Order', mo.name, 'erpnext_wo', new_doc.name)

		frappe.msgprint(_("Manufacturing order exported successfully."))

	else:
		frappe.msgprint(_("Duplicate manufacturing order. Manufacturing order is not created"))




# Sync the status of work order in erpnext with the manufacturing order in frepple
@frappe.whitelist()
def update_frepple_mo_status(doc):
	doc = json.loads(doc)
	if (frappe.get_doc("Frepple Settings").frepple_integration) and doc["docstatus"]:
		wo = frappe.get_doc("Work Order",doc["name"]) #ERPNext work order
		print(wo)
		mos = frappe.db.sql(
			"""
			SELECT name,erpnext_wo
			FROM `tabFrepple Manufacturing Order`
			WHERE erpnext_wo = %s
			""",
		wo.name,as_dict=1)

		for mo in mos:
			# mo = frappe.db.get_list('Frepple Manufacturing Order', filters={
			# 	'erpnext_wo': [wo.name]	
			# }) # Get the frepple manufacturing order with owner work order match

			# print(mo[0])
			frappe.db.set_value('Frepple Manufacturing Order', mo.name, 'status',mo_status_e2f(wo.status)) #Update the status
			print(mo_status_e2f(wo.status))

# CHeck the erpnext work order status and get its correspond frepple manufacturing order status
# ERPNExt -> Frepple
def mo_status_e2f(status):
	switcher={
		"Draft":'proposed',
		"Submitted":'confirmed',
		"Not Started":'confirmed',
		"In Process":'confirmed',
		"Stopped":'closed',
		"Completed":'completed',
		"Cancelled":'closed',	
	}
	return switcher.get(status,"proposed") #default is "proposed" status

	'ERPNext'				'Frepple'
	# Draft					proposed
	# Submitted				confirmed
	# Not Started			completed
	# In Process			approved
	# Stopped				cancelled
	# Completed
	# Cancelled

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
