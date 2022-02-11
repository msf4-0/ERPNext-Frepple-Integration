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
		import_datas.append("Frepple Calendar")
	if doc["frepple_calendar_bucket"]:
		export_calendar_buckets()
		import_datas.append("Frepple Calendar Bucket")

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
		export_suppliers()
		import_datas.append("Frepple Supplier")
	if doc["frepple_item_supplier"]:
		export_item_suppliers()
		import_datas.append("Frepple Item Supplier")
	
	# Manufacturing
	if doc["frepple_operation"]:
		export_operations()
		import_datas.append("Frepple Operation")
	if doc["frepple_operation_material"]:
		export_operation_materials()
		import_datas.append("Frepple Operation Materials")

	if doc["frepple_operation_resource"]:
		export_operation_resources()
		import_datas.append("Frepple Operation Resource")

	if doc["frepple_demand"]:
		export_sales_orders()
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


def export_calendars():
	api = "calendar"
	url,headers = get_frepple_params(api=api,filter=None)

	calendars = frappe.db.sql(
		"""
		SELECT calendar_name,default_value 
		FROM `tabFrepple Calendar`""",
		as_dict=1
	)

	for calendar in calendars:
		data = json.dumps({
			"name": calendar.calendar_name,
			"defaultvalue":calendar.default_value
		})
		output = make_post_request(url,headers=headers, data=data)
	

def export_calendar_buckets():
	api = "calendarbucket"
	url,headers = get_frepple_params(api=api,filter=None)

	calendar_buckets = frappe.db.sql(
		"""
		SELECT calendar,value,priority, timestamp(start_datetime) as "start_datetime",timestamp(end_datetime) as "end_datetime",
		timestamp(start_time) as "start_time",timestamp(end_time) as "end_time",
		monday, tuesday, wednesday, thursday, friday, saturday, sunday
		FROM `tabFrepple Calendar Bucket`""",
		as_dict=1
	)

	for calendar_bucket in calendar_buckets:
		print(calendar_bucket)
		print(calendar_bucket.start_datetime.isoformat())
		data = json.dumps({
			"calendar": calendar_bucket.calendar,
			"startdate": calendar_bucket.start_datetime.isoformat(),
			"enddate":calendar_bucket.end_datetime.isoformat() ,
			"value": calendar_bucket.value,
			"priority": calendar_bucket.priority,
			"monday": "true" if calendar_bucket.monday else "false",
			"tuesday": "true" if calendar_bucket.tuesday else "false",
			"wednesday": "true" if calendar_bucket.wednesday else "false",
			"thursday": "true" if calendar_bucket.thursday else "false",
			"friday": "true" if calendar_bucket.friday else "false",
			"saturday": "true" if calendar_bucket.saturday else "false",
			"sunday": "true" if calendar_bucket.sunday else "false",
			"starttime": str(calendar_bucket.start_time.time()),
			"endtime":str(calendar_bucket.end_time.time())
		})
		output = make_post_request(url,headers=headers, data=data)
	

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
	

	

def export_locations():
	api = "location"
	url,headers = get_frepple_params(api=api,filter=None)

	locations = frappe.db.sql("""SELECT warehouse, location_owner, available FROM `tabFrepple Location`""",as_dict=1)
	
	for location in locations:
		print(location)

		if location.available:
			available = location.available
		else:
			available = None

		# If the location is a child location
		if (location.location_owner != None):
			# Create the company document in frepple first
			data = json.dumps({
				"name": location.location_owner,
			})
			output = make_post_request(url,headers=headers, data=data)

			data = json.dumps({
				"name": location.warehouse,
				"available":available,
				"owner":location.location_owner, 
			})
			output = make_post_request(url,headers=headers, data=data)

		# If the location is a parent
		else:
			print(available)
			data = json.dumps({
				"name": location.warehouse,
				"available":available
			})
			output = make_post_request(url,headers=headers, data=data)


	

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
	


def export_item_distribution():
	api = "itemdistribution"
	url,headers = get_frepple_params(api=api,filter=None)


	distributions = frappe.db.sql(
		"""
		SELECT item,origin,destination,day,timestamp(time) as "time" 
		FROM `tabFrepple Item Distribution`
		""",
	as_dict=1)

	for distribution in distributions:
		print(distribution)
		data = json.dumps({
			"item": distribution.item,
			"origin":distribution.origin,
			"location":distribution.destination,
			"leadtime":str(distribution.day)+" "+str(distribution.time.time())
		})
		output = make_post_request(url,headers=headers, data=data)


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

		if resource.available:
			available = resource.available
		else:
			available = None
		
		'''Add the actual employee to frepple'''
		data = json.dumps({
			"name": resource.name1,
			"available":available,
			"type":resource.type,
			"maximum":resource.maximum,
			"description":resource.description,
			"location":resource.location,
			"owner":resource.resource_owner #default
		})
		output = make_post_request(url,headers=headers, data=data)
	

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

	
def export_suppliers():
	api = "supplier" #equivalent to customer doctype		
	url,headers = get_frepple_params(api=api,filter=None)
	

	suppliers = frappe.db.sql(
		"""
		SELECT supplier 
		FROM `tabFrepple Supplier`
		""",
	as_dict=1)
	for supplier in suppliers:
		data = json.dumps({
			"name": supplier.supplier,
		})

		output = make_post_request(url,headers=headers, data=data)
		

def export_item_suppliers():
	api = "itemsupplier"
	url,headers = get_frepple_params(api=api,filter=None)
	item_suppliers = frappe.db.sql(
		"""
		SELECT supplier, item, supplier_cost, day, timestamp(time) as "time"
		FROM `tabFrepple Item Supplier`
		""",
	as_dict=1)
	
	#timestamp() sql method give us datetime type. So we can use datetime method time() to get time
	# date() to get date 

	for item_supplier in item_suppliers:
		# if item_supplier.time:
		# 	time = str(item_supplier.time.time())
		# else:
		# 	time = "null"

		print(item_supplier)
		# print(str(item_supplier.day)+" "+str(item_supplier.time.time()))
		data = json.dumps({
			"supplier":item_supplier.supplier,
			"item":item_supplier.item,
			"cost":item_supplier.supplier_cost,
			"leadtime":str(item_supplier.day)+" "+str(item_supplier.time.time())
			# "duration_per":(datetime(1900,1,1,0,0,0)+ operation.duration_per_unit).time(), 
		})

		output = make_post_request(url,headers=headers, data=data)
		


def export_operations():
	api = "operation"
	url,headers = get_frepple_params(api=api,filter=None)
	
	routing_operations = frappe.db.sql(
		"""
		SELECT operation, item, location, type, priority,timestamp(duration_per_unit) as "duration_per_unit", timestamp(duration) as "duration",operation_owner
		FROM `tabFrepple Operation`
		WHERE type = "routing"
		""",
		as_dict=1)
	
	print(routing_operations)
	for operation in routing_operations:
	
		if operation.duration:
			duration = str(operation.duration.time())
		else:
			duration = "null"
		
		data = json.dumps({
			"name":operation.operation,
			"item":operation.item,
			"location":operation.location,
			"type":operation.type,
			"priority":operation.priority,
			# "duration_per":(datetime(1900,1,1,0,0,0)+ operation.duration_per_unit).time(), 
			"duration":duration,
			
		})
		
		output = make_post_request(url,headers=headers, data=data)
	
	time_per_operations = frappe.db.sql(
		"""
		SELECT operation, item, location, type, priority,timestamp(duration_per_unit) as "duration_per_unit", timestamp(duration) as "duration",operation_owner
		FROM `tabFrepple Operation`
		WHERE type = "time_per"
		""",
	as_dict=1)
	
	for operation in time_per_operations:

		print(type(operation.duration_per_unit))
		if operation.duration:
			duration = str(operation.duration.time())
		else:
			duration = "null"

		data = json.dumps({
			"name":operation.operation,
			"type":operation.type,
			"priority":operation.priority,
			"location":operation.location,
			# "duration_per":(datetime(1900,1,1,0,0,0)+ operation.duration_per_unit).time(), 
			"duration_per":str(operation.duration_per_unit.time()),
			"duration":duration,
			"owner":operation.operation_owner
		})
		output = make_post_request(url,headers=headers, data=data)


def export_operation_materials():
	api = "operationmaterial"
	url,headers = get_frepple_params(api=api,filter=None)

	materials = frappe.db.sql(
		"""
		SELECT operation, item, quantity, type
		FROM `tabFrepple Operation Material`
		""",
	as_dict=1)
	
	for material in materials:
		print(material)
		data = json.dumps({
			"operation":material.operation,
			"item":material.item,
			"quantity":material.quantity,
			"type":material.type
		})
		output = make_post_request(url,headers=headers, data=data)


def export_operation_resources():
	api = "operationresource"
	url,headers = get_frepple_params(api=api,filter=None)

	employee_resources = frappe.db.sql(
		"""
		SELECT operation,employee_check,resource,quantity,skill 
		FROM `tabFrepple Operation Resource`
		WHERE employee_check = 1
		""",
	as_dict=1)

	for resource in employee_resources:
		print(resource)
		# if HUman Resource, then we let resource = "Operator"
		data = json.dumps({
			"operation":resource.operation,
			"resource":"Operator",
			"quantity":resource.quantity,
			"skill":resource.skill
		})
		output = make_post_request(url,headers=headers, data=data)

	workstation_resources = frappe.db.sql(
		"""
		SELECT operation,employee_check,resource,quantity 
		FROM `tabFrepple Operation Resource`
		WHERE employee_check = 0
		""",
	as_dict=1)

	for resource in workstation_resources:
		print(resource)
		data = json.dumps({
			"operation":resource.operation,
			"resource":resource.resource,
			"quantity":resource.quantity,
		})
		output = make_post_request(url,headers=headers, data=data)

def export_sales_orders():
	api = "demand" #equivalent sales order
	url,headers = get_frepple_params(api=api,filter=None)
	
	sales_orders = frappe.db.sql(
		"""
		SELECT name,item,item_name,qty,location,customer, timestamp(due) as "due",priority,status,so_owner
		FROM `tabFrepple Demand`
		""",
	as_dict=1)

		
	for sales_order in sales_orders:
		print(sales_order)
		data = json.dumps({
			"name": sales_order.name,
			"description": sales_order.item_name + " ordered by " + sales_order.customer, #default
			"item": sales_order.item,
			"customer": sales_order.customer,
			"location": sales_order.location,
			"due":  sales_order.due.isoformat(),
			"status": sales_order.status,
			"quantity": sales_order.qty,
			"priority": sales_order.priority
		})

		output = make_post_request(url,headers=headers, data=data)



# def export_manufacturing_orders():
# 	api = "manufacturingorder" #equivalent work order
# 	url,headers = get_frepple_params(api=api,filter=None)
	
# 	sales_orders = frappe.db.sql(
# 		"""
# 		SELECT reference,operation,status,qty,location,customer, timestamp(due) as "due",priority,status,so_owner
# 		FROM `tabFrepple Manufacturing Order`
# 		""",
# 	as_dict=1)

		
# 	for sales_order in sales_orders:
# 		print(sales_order)
# 		data = json.dumps({
# 			"name": sales_order.name,
# 			"description": sales_order.item_name + " ordered by " + sales_order.customer, #default
# 			"item": sales_order.item,
# 			"customer": sales_order.customer,
# 			"location": sales_order.location,
# 			"due":  sales_order.due.isoformat(),
# 			"status": sales_order.status,
# 			"quantity": sales_order.qty,
# 			"priority": sales_order.priority
# 		})

# 		output = make_post_request(url,headers=headers, data=data)
