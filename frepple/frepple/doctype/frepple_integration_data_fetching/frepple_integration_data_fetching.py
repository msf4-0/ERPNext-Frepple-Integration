# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,json
from frappe.model.document import Document
from frappe import _

from datetime import datetime
from datetime import time
from datetime import timedelta
from frappe.utils import add_to_date

class FreppleIntegrationDataFetching(Document):
	pass

@frappe.whitelist()
def fetch_data(doc):
	doc = json.loads(doc)

	import_datas = []
	# Sales
	if doc["frepple_item"]:
		fetch_items()
		import_datas.append("Frepple Item")
	if doc["frepple_customer"]:
		fetch_customers()
		import_datas.append("Frepple Customer")
	if doc["frepple_location"]:
		fetch_locations()
		import_datas.append("Frepple Location")

	# Inventory
	if doc["frepple_buffer"]:
		fetch_buffer()
	# if doc["frepple_item_distribution"]:
		# fetch_item_distribution()


	# Capacity
	if doc["frepple_resource"]:
		fetch_resources()
		import_datas.append("Frepple Resource")
	if doc["frepple_skill"]:
		fetch_skills()
		import_datas.append("Frepple Skill")
	# HAVENT include yet
	if doc["frepple_resource_skill"]:
		fetch_resource_skills()
		import_datas.append("Frepple Resource Skill")

	# Purchasing
	if doc["frepple_supplier"]:
		fetch_suppliers()
		import_datas.append("Frepple Supplier")
	if doc["frepple_item_supplier"]:
		fetch_item_suppliers()
		import_datas.append("Frepple Item Supplier")
	
	# Manufacturing
	if doc["frepple_operation"]:
		fetch_operations()
		import_datas.append("Frepple Operation")
	if doc["frepple_operation_material"]:
	 	fetch_operation_materials()
		# import_datas.append("Frepple Operation Materials")
	if doc["frepple_operation_resource"]:
		return fetch_operation_resources()
		import_datas.append("Frepple Operation Resource")

	# Output msg 
	for import_data in import_datas:
		frappe.msgprint(_("{0} is imported.").format(import_data))


def fetch_items():
	items = frappe.db.sql("""SELECT item_code, item_name, item_group, valuation_rate, stock_uom FROM `tabItem`""",as_dict=1)
	for item in items:
		if not frappe.db.exists("Frepple Item",item.item_code):
			new_item = frappe.new_doc("Frepple Item")
			new_item.item = item.item_code
			new_item.description = item.item_name
			new_item.uom = item.stock_uom
			new_item.cost = item.valuation_rate
			new_item.item_owner = item.item_group
			new_item.insert()

def fetch_customers():
	customers = frappe.db.sql("""SELECT name, customer_group, customer_type FROM `tabCustomer`""",as_dict=1)
	for customer in customers:
		if not frappe.db.exists("Frepple Customer",customer.name):
			new_customer = frappe.new_doc("Frepple Customer")
			new_customer.customer = customer.name
			new_customer.customer_group = customer.customer_group
			new_customer.customer_type = customer.customer_type
			new_customer.insert()

	# frappe.msgprint(
	# 	msg='.',
	# 	title='Note',
	# )

def fetch_locations():
	locations = frappe.db.sql("""SELECT name FROM `tabWarehouse`""",as_dict=1)
	for location in locations:
		if not frappe.db.exists("Frepple Location",location.name):
			new_location = frappe.new_doc("Frepple Location")
			new_location.warehouse = location.name
			new_location.insert()



def fetch_resources():
	employees = frappe.db.sql("""SELECT name, employee_name FROM `tabEmployee`""",as_dict=1)
	locations = frappe.db.sql(
	"""
	SELECT name FROM `tabFrepple Location`
	WHERE name LIKE 'Work In Progress%%'
	""",
	as_dict=1)
	for employee in employees:
		if not frappe.db.exists("Frepple Resource",employee.name):
			new_employee = frappe.new_doc("Frepple Resource")
			new_employee.employee = employee.name
			new_employee.descrption = employee.employee_name
			new_employee.location = locations[0].name
			new_employee.resource_owner = "Operator" #default

			new_employee.name1 = employee.name
			new_employee.employee_check = 1
			new_employee.insert()
	
	# workstations = frappe.db.sql("""SELECT ws.name, fl.name FROM `tabWorkstation` ws, `tabFrepple Location` fl""",as_dict=1)
	workstations = frappe.db.sql(
		"""
		SELECT name FROM `tabWorkstation`
		""",
		as_dict=1)
	for workstation in workstations:
		if not frappe.db.exists("Frepple Resource",workstation.name):
			new_workstation = frappe.new_doc("Frepple Resource")
			new_workstation.workstation = workstation.name
			new_workstation.location = locations[0].name
			new_workstation.resource_owner = "Workstation" #default

			new_workstation.name1 = workstation.name
			new_workstation.workstation_check = 1
			new_workstation.insert()

def fetch_skills():
	skills = frappe.db.sql("""SELECT name FROM `tabSkill`""",as_dict=1)
	for skill in skills:
		if not frappe.db.exists("Frepple Skill",skill.name):
			new_skill = frappe.new_doc("Frepple Skill")
			new_skill.skill = skill.name
			new_skill.insert()


''' Under progress'''
# def fetch_resource_skills():
# 	employee_skill_list = frappe.db.sql("""SELECT name,employee_skills FROM `tabEmployee Skill Map`""",as_dict=1)

# 	if (employee_skill_list):
# 		for employee_skill in employee_skill_list:

# 			if not frappe.db.exists("Frepple Resource Skill",name+"@"+employee_skills):
# 				new_resource_skill = frappe.new_doc("Frepple Resource Skill")
# 				# new_resource_skill.skill = employee_skill.
# 				# new_employee.insert()


def fetch_suppliers():
	suppliers = frappe.db.sql("""SELECT name FROM `tabSupplier`""",as_dict=1)
	for supplier in suppliers:
		if not frappe.db.exists("Frepple Supplier",supplier.name):
			new_supplier = frappe.new_doc("Frepple Supplier")
			new_supplier.supplier = supplier.name
			new_supplier.insert()

''' Under progress'''
# def fetch_supplier_items():
# 	suppliers = frappe.db.sql("""SELECT name FROM `tabSupplier`""",as_dict=1)
# 	for supplier in suppliers:
# 		if not frappe.db.exists("Frepple Supplier",supplier.name):
# 			new_supplier = frappe.new_doc("Frepple Supplier")
# 			new_supplier.supplier = supplier.name
# 			new_supplier.insert()


def fetch_operations():
	locations = frappe.db.sql(
		"""
		SELECT name FROM `tabFrepple Location`
		WHERE name LIKE 'Work In Progress%%'
		""",
		as_dict=1)
	BOMs = frappe.db.sql(
		"""
		SELECT bom.name, bom.is_active, bom.is_default, bomop.operation, bomop.workstation, bomop.time_in_mins,bomit.item_code 
		FROM `tabBOM` bom, `tabBOM Operation` bomop,`tabBOM Item` bomit
		WHERE bom.is_active = 1 and bom.is_default and bom.name = bomop.parent and bom.name = bomit.parent
		""",
		as_dict=1)
	

	for BOM in BOMs:
		if not frappe.db.exists("Frepple Operation",BOM.name):
			new_operation = frappe.new_doc("Frepple Operation")
			new_operation.operation = BOM.name
			new_operation.location = locations[0].name
			new_operation.type = "routing"
			new_operation.item = BOM.item_code
			new_operation.duration = time(0,0,0)
			new_operation.priority = 1
			new_operation.insert()

		if not frappe.db.exists("Frepple Operation",BOM.operation+"@"+BOM.name):
			new_operation = frappe.new_doc("Frepple Operation")
			new_operation.operation = BOM.operation+"@"+BOM.name
			new_operation.location = locations[0].name
			new_operation.type = "time_per"
			new_operation.operation_owner = BOM.name
			new_operation.duration = time(0,0,0)
			new_operation.duration_per_unit=add_to_date(datetime(1900,1,1,0,0,0),minutes=(BOM.time_in_mins),as_datetime=True).time() #get only the time
			new_operation.insert()



	# for BOM in BOMs:
	# 	if not frappe.db.exists("Frepple Operation",BOMs.name):
	# 		new_operation = frappe.new_doc("Frepple Operation")
			
	# 		new_operation.insert()


def fetch_operation_materials():
	BOMs = frappe.db.sql(
		"""
		SELECT bom.name, bom.item,bom.quantity, bom.transfer_material_against, bom.is_active, bom.is_default,bomop.operation,bomit.item_code,bomit.qty 
		FROM `tabBOM` bom, `tabBOM Operation` bomop,`tabBOM Item` bomit
		WHERE bom.is_active = 1 and bom.is_default=1 and bom.name = bomop.parent and bom.name = bomit.parent
		""",
	as_dict=1)
	frepple_operations = frappe.db.sql(
		"""
		SELECT name,type
		FROM `tabFrepple Operation`
		WHERE type = "time_per"
		""",
	as_dict=1)


	for BOM in BOMs:
		if (BOM.transfer_material_against == "Work Order"): #let the first operation consumed raw material and produce product
			# for item in BOM.item_code:
			# For product which is being produced
			if not frappe.db.exists("Frepple Operation Material",BOM.item+"-"+frepple_operations[0].name):
				new_operation_material = frappe.new_doc("Frepple Operation Material")
				new_operation_material.operation = frepple_operations[0].name
				new_operation_material.item = BOM.item
				new_operation_material.type = "End"
				new_operation_material.quantity = BOM.quantity
				new_operation_material.insert()

			# For raw materials which is being consumed
			if not frappe.db.exists("Frepple Operation Material",BOM.item_code+"-"+frepple_operations[0].name):
				new_operation_material = frappe.new_doc("Frepple Operation Material")
				new_operation_material.operation = frepple_operations[0].name
				new_operation_material.item = BOM.item_code
				new_operation_material.type = "Start"
				new_operation_material.quantity = BOM.qty
				new_operation_material.insert()


	''' NOT YET CONSIDER the case if material transfer type is "JOB card" where each operation got their own type'''
		# if (BOM.transfer_material_against == "Job Card"): #assign material to the correspond operation

		# if not frappe.db.exists("Frepple Operation",BOM.operation+"@"+BOM.name):
		# 	new_operation = frappe.new_doc("Frepple Operation")
		# 	new_operation.operation = BOM.operation+"@"+BOM.name
		# 	new_operation.location = locations[0].name
		# 	new_operation.type = "time_per"
		# 	new_operation.operation_owner = BOM.name
		# 	new_operation.duration = time(0,0,0)
		# 	new_operation.duration_per_unit=add_to_date(datetime(1900,1,1,0,0,0),minutes=(BOM.time_in_mins),as_datetime=True).time() #get only the time
		# 	new_operation.insert()



	# for BOM in BOMs:
	# 	if not frappe.db.exists("Frepple Operation",BOMs.name):
	# 		new_operation = frappe.new_doc("Frepple Operation")
			
	# 		new_operation.insert()


def fetch_operation_resources():
	BOMs = frappe.db.sql(
		"""
		SELECT bom.name, bom.is_active, bom.is_default, bomop.operation, bomop.workstation 
		FROM `tabBOM` bom, `tabBOM Operation` bomop
		WHERE bom.is_active = 1 and bom.is_default=1 and bomop.parent = bom.name
		""",
	as_dict=1)

	for BOM in BOMs:
		if not frappe.db.exists("Frepple Operation Resource",BOM.operation+"@"+BOM.name):
			new_doc = frappe.new_doc("Frepple Item")
			new_doc.operation = BOM.operation+"@"+BOM.name
			new_doc.resource = BOM.workstation
		if frappe.db.exists("Frepple Resource",BOM.workstation) and frappe.db.exists("Frepple Operation",BOM.operation+"@"+BOM.name):
			new_doc.insert()

	frepple_operations = frappe.db.sql(
		"""
		SELECT name,type
		FROM `tabFrepple Operation`
		WHERE type = "time_per"
		""",
	as_dict=1)
	print(BOMs)
	# Get the workstation


	# BOMs = frappe.db.get_list('BOM',
	# 	filters={
	# 		'is_active': 1,
	# 		"is_default": 1
	# 	},
	# )
	# doc = frappe.get_doc("BOM",BOMs[0].name)

	# return doc.operations
	# # for BOM in BOMs:
	# for row in doc.operations:
	# 	d = frappe.get_doc('BOM Operation', row.name) #To access child doctype
			
		
