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

from frappe.integrations.utils import make_get_request, make_post_request, create_request_log
from frappe.utils import get_request_session

import requests
from requests.structures import CaseInsensitiveDict

class FreppleDataExport(Document):
	pass


@frappe.whitelist()
def export_data(doc):
	doc = json.loads(doc)

	import_datas = []

	#Additional data
	if doc["frepple_calendar"]:
		export_calendars()

	if doc["frepple_calendar_bucket"]:
		export_calendar_buckets()

	# Sales
	if doc["frepple_item"]:
		export_items()
		import_datas.append("Frepple Item")
	if doc["frepple_customer"]:
		export_customers()
		import_datas.append("Frepple Customer")
	if doc["frepple_location"]:
		export_locations()
		import_datas.append("Frepple Location")

	# Inventory
	if doc["frepple_buffer"]:
		export_buffers()
	if doc["frepple_item_distribution"]:
		export_item_distribution()


	# Capacity
	if doc["frepple_resource"]:
		export_resources()
		import_datas.append("Frepple Resource")
	if doc["frepple_skill"]:
		export_skills()
		import_datas.append("Frepple Skill")
	# HAVENT include yet
	if doc["frepple_resource_skill"]:
		export_resource_skills()
		import_datas.append("Frepple Resource Skill")

	# Purchasing
	if doc["frepple_supplier"]:
		return export_suppliers()
		import_datas.append("Frepple Supplier")
	if doc["frepple_item_supplier"]:
		return export_item_suppliers()
		import_datas.append("Frepple Item Supplier")
	
	# Manufacturing
	if doc["frepple_operation"]:
		return export_operations()
		import_datas.append("Frepple Operation")
	if doc["frepple_operation_material"]:
		return export_operation_materials()
		import_datas.append("Frepple Operation Materials")

	if doc["frepple_operation_resource"]:
		return export_operation_resources()
		import_datas.append("Frepple Operation Resource")

	if doc["frepple_demand"]:
		return export_sales_orders()
		import_datas.append("Frepple Demand")

	# Output msg 
	for import_data in import_datas:
		frappe.msgprint(_("{0} is exported.").format(import_data))

@frappe.whitelist()
def get_frepple_params(api=None,filter = None):
	if not api:
		api = "" #default get the demand(=sales order in ERPNext) list from frepple
	if not filter:
		filter = ""

	frepple_settings = frappe.get_doc("Frepple Settings")
	temp_url = frepple_settings.url.split("//")
	url1 = "http://"+ frepple_settings.username + ":" + frepple_settings.password + "@" + temp_url[1] + "/api/input/"
	url2 = "/"
	# "/?format=json"
	# "/?format=api"

	#Concatenate the URL
	url = url1 +  api + url2 + filter
	# example outcome : http://admin:admin@192.168.112.1:5000/api/input/manufacturingorder/

	headers= {
		'Content-type': 'application/json; charset=UTF-8',
		'Authorization': frepple_settings.authorization_header,
	}
	print(url+ "-------------------------------------------------------------------------")

	return url,headers

def export_items():
	api = "item" 
	
	url,headers = get_frepple_params(api=api,filter=None)

	items = frappe.db.sql("""SELECT item, description, stock_uom, valuation_rate, item_group FROM `tabFrepple Item`""",as_dict=1)
	
	for item in items:
		'''Add the item_group to frepple to use it as the owner to ensure no request error happen'''
		data = json.dumps({
			"name": item.item_group
		})
		output = make_post_request(url,headers=headers, data=data)

		'''Add the actual item to frepple'''
		data = json.dumps({
			"name": item.item,
			"owner":item.item_group,
			"description":item.description,
			"uom":item.stock_uom,
			"cost":item.valuation_rate,
		})
		output = make_post_request(url,headers=headers, data=data)
	
	return output

def export_customers():
	api = "customer"
	url,headers = get_frepple_params(api=api,filter=None)

	customers = frappe.db.sql("""SELECT name, customer_group, customer_type FROM `tabFrepple Customer`""",as_dict=1)
	for customer in customers:
		'''Add the customer_group to frepple to use it as the owner to ensure no request error happen'''
		data = json.dumps({
			"name": customer.customer_group
		})
		output = make_post_request(url,headers=headers, data=data)

		'''Add the actual customer to frepple'''
		data = json.dumps({
			"name": customer.name,
			"category":customer.customer_type,
			"owner":customer.customer_group
		})
		output = make_post_request(url,headers=headers, data=data)
	

	return output
	

def export_locations():
	api = "location"
	url,headers = get_frepple_params(api=api,filter=None)

	locations = frappe.db.sql("""SELECT warehouse, location_owner, available FROM `tabFrepple Location`""",as_dict=1)
	
	print(locations)
	for location in locations:
		print(location)
		# If the location is a child location
		if (location.location_owner != None):
			data = json.dumps({
				"name": location.location_owner,
				# "available":location.available
			})
			output = make_post_request(url,headers=headers, data=data)

			data = json.dumps({
				"name": location.warehouse,
				# "available":location.available,
				"owner":location.location_owner, 
			})
			output = make_post_request(url,headers=headers, data=data)
		# If the location is a parent
		if (location.location_owner == None):
			data = json.dumps({
				"name": location.warehouse,
				# "available":location.available
			})
			output = make_post_request(url,headers=headers, data=data)

	return output

	

def export_buffers():
	api = "buffer"
	url,headers = get_frepple_params(api=api,filter=None)

	buffers = frappe.db.sql(
		"""
		SELECT item, location, onhand FROM `tabFrepple Buffer`
		""",
		as_dict=1)
	for buffer in buffers:
		data = json.dumps({
			"item":buffer.item,
			"location": buffer.location,
			"onhand": buffer.onhand,
		})
		output = make_post_request(url,headers=headers, data=data)
	
	return output


def export_item_distribution():

	return True


def export_resources():
	api = "resource" #equivalent to employee doctype
	url,headers = get_frepple_params(api=api,filter=None)
			
	resources = frappe.db.sql(
		"""
		SELECT name1, location,available, type, maximum,description,resource_owner 
		FROM `tabFrepple Resource`
		""",as_dict=1)

	for resource in resources:
		print(resource)
	# For human resource
		'''Add a null operator or workstation to frepple to use it as the owner to ensure no request error happen'''
		data = json.dumps({
			"name": resource.resource_owner,#default
		})
		output = make_post_request(url,headers=headers, data=data)

		'''Add the actual employee to frepple'''
		data = json.dumps({
			"name": resource.name1,
			# "available":resource.available,
			"type":resource.type,
			"maximum":resource.maximum,
			"description":resource.description,
			"location":resource.location,
			"owner":resource.resource_owner #default
			
		
		})
		output = make_post_request(url,headers=headers, data=data)
	
	return output

def export_skills():
	api = "skill" 
	url,headers = get_frepple_params(api=api,filter=None)

	skills = frappe.db.sql("""SELECT skill FROM `tabFrepple Skill`""",as_dict=1)
	for skill in skills:
		print(skill)
		data = json.dumps({
			"name": skill.skill,
		})

		output = make_post_request(url,headers=headers, data=data)




def export_resource_skills():
	api = "resourceskill" #equivalent to customer doctype
	url,headers = get_frepple_params(api=api,filter=None)
		
	employee_skill_list = frappe.db.sql("""SELECT resource,skill, priority FROM `tabFrepple Resource Skill`""",as_dict=1)
	
	for employee_skill in employee_skill_list:
		data = json.dumps({
			"resource": employee_skill.resource,
			"skill":employee_skill.skill,
			"priority":5-employee_skill.priority
		})

	output = make_post_request(url,headers=headers, data=data)

	return output
	


def export_suppliers():
	api = "supplier" #equivalent to customer doctype		
	url,headers = get_frepple_params(api=api,filter=None)
	

	suppliers = frappe.db.sql("""SELECT supplier FROM `tabFrepple Supplier`""",as_dict=1)
	for supplier in suppliers:
		data = json.dumps({
			"name": supplier.supplier,
		})

		output = make_post_request(url,headers=headers, data=data)
		
''' Under progress'''
# def export_supplier_items():
# 	suppliers = frappe.db.sql("""SELECT name FROM `tabSupplier`""",as_dict=1)
# 	for supplier in suppliers:
# 		if not frappe.db.exists("Frepple Supplier",supplier.name):
# 			new_supplier = frappe.new_doc("Frepple Supplier")
# 			new_supplier.supplier = supplier.name
# 			new_supplier.insert()


def export_operations():
	api = "operation"
	url,headers = get_frepple_params(api=api,filter=None)
	
	routing_operations = frappe.db.sql(
		"""
		SELECT operation, item, location, type, priority,timestamp(duration_per_unit) as "duration_per_unit", duration,operation_owner
		FROM `tabFrepple Operation`
		WHERE type = "routing"
		""",
		as_dict=1)
	
	print(routing_operations)
	for operation in routing_operations:
	

		data = json.dumps({
			"name":operation.operation,
			"item":operation.item,
			"location":operation.location,
			"type":operation.type,
			"priority":operation.priority,
			# "duration_per":(datetime(1900,1,1,0,0,0)+ operation.duration_per_unit).time(), 
			# "duration":operation.duration,
			
		})
		
		output = make_post_request(url,headers=headers, data=data)
	
	time_per_operations = frappe.db.sql(
		"""
		SELECT operation, item, location, type, priority,timestamp(duration_per_unit) as "duration_per_unit", duration,operation_owner
		FROM `tabFrepple Operation`
		WHERE type = "time_per"
		""",
	as_dict=1)
	
	for operation in time_per_operations:
		# print(operation)
		# print(str(operation.duration_per_unit.time()))
		# print(operation.item)
		# abc = operation.item if operation.item else " "
		# print(abc)

		data = json.dumps({
			"name":operation.operation,
			"type":operation.type,
			"priority":operation.priority,
			"location":operation.location,
			# "duration_per":(datetime(1900,1,1,0,0,0)+ operation.duration_per_unit).time(), 
			"duration_per":str(operation.duration_per_unit.time()),
			# "duration":operation.duration,
			"owner":operation.operation_owner
		})
		output = make_post_request(url,headers=headers, data=data)

	return output

def export_operation_materials():
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
				new_operation_material.quantity = BOM.qty * -1 #consumed item need to be negative
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


def export_operation_resources():
	BOMs = frappe.db.sql(
		"""
		SELECT bom.name, bom.is_active, bom.is_default, bomop.operation, bomop.workstation 
		FROM `tabBOM` bom, `tabBOM Operation` bomop
		WHERE bom.is_active = 1 and bom.is_default=1 and bomop.parent = bom.name
		""",
	as_dict=1)


	for BOM in BOMs:
		if not frappe.db.exists("Frepple Operation Resource",BOM.workstation+"-"+BOM.operation+"@"+BOM.name):
			new_doc = frappe.new_doc("Frepple Operation Resource")
			new_doc.operation = BOM.operation+"@"+BOM.name
			new_doc.resource = BOM.workstation
			if frappe.db.exists("Frepple Resource",BOM.workstation) and frappe.db.exists("Frepple Operation",BOM.operation+"@"+BOM.name):
				new_doc.insert()


def export_sales_orders():
	sales_orders = frappe.db.sql(
		"""
		SELECT so.name, so.company, so.status, so.delivery_date, so.customer,soi.item_code, soi.qty, soi.work_order_qty  
		FROM `tabSales Order` so, `tabSales Order Item` soi
		WHERE soi.parent = so.name and soi.work_order_qty < 1"
		""",
	as_dict=1)
	print(sales_orders)

		
	for sales_order in sales_orders:
		frepple_demand = frappe.db.sql(
			"""
			SELECT name  
			FROM `tabFrepple Demand`
			WHERE name like %s 
			""",
		(sales_order.name+'%'), as_dict=1)

		if not len(frepple_demand):
			new_demand = frappe.new_doc("Frepple Demand")
			new_demand.item = sales_order.item_code
			new_demand.qty = sales_order.qty
			new_demand.location = sales_order.company
			new_demand.customer = sales_order.customer
			new_demand.due =  sales_order.delivery_date
			new_demand.so_owner =  sales_order.name
			# if frappe.db.exists("Frepple Resource",BOM.workstation) and frappe.db.exists("Frepple Operation",BOM.operation+"@"+BOM.name):
			new_demand.insert()
