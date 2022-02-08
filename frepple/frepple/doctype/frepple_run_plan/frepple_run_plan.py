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

from frepple.frepple.doctype.frepple_data_export.frepple_data_export import get_frepple_params,export_sales_orders

class FreppleRunPlan(Document):
	pass

@frappe.whitelist()
def run_plan(doc):
	doc = json.loads(doc)

	if doc["update_frepple"]:
		export_sales_orders()
		export_manufacturing_orders()
		export_purchase_orders()

	constraint= 0
	plantype = 1
	# filter = "/execute/api/runplan/?"
	
	if doc['constraint']:
		plantype = 1
	if doc['unconstraint']:
		plantype = 2
	if doc['capacity']:
		constraint = constraint + 4
	if doc['lead_time']:
		constraint = constraint + 1
	if doc['release_fence']:
		constraint = constraint + 8

	filter = "/execute/api/runplan/?constraint="+ str(constraint)+"&plantype="+ str(plantype)+"&env=supply"
	frepple_settings = frappe.get_doc("Frepple Settings")
	temp_url = frepple_settings.url.split("//")
	url = "http://"+ frepple_settings.username + ":" + frepple_settings.password + "@" + temp_url[1] + filter
	print(url + "-----------------------------------------------------------------------")
	headers= {
		'Content-type': 'application/json; charset=UTF-8',
		'Authorization': frepple_settings.authorization_header,
	}

	output = make_post_request(url,headers=headers, data=None)

	frappe.msgprint(
		msg='Plan have been runned successfully.',
		title='Success',
	)

	return output

@frappe.whitelist()
def generate_result(doc):
	
	import_datas = []
	# Import manufacturing order
	data = import_manufacturing_order()
	# return data
	import_datas.append("Manufacturing Order Result")
	generate_manufacturing_order(data)

	# Import purchase order
	data = import_purchase_order()
	import_datas.append("Purchase Order Result")
	generate_purchase_order(data)

	# Output msg 
	for import_data in import_datas:
		frappe.msgprint(_("{0} is imported.").format(import_data))


def export_manufacturing_orders():
	api = "manufacturingorder" #equivalent work order
	url,headers = get_frepple_params(api=api,filter=None)
	
	mos = frappe.db.sql(
		"""
		SELECT latest_reference,operation,status,quantity
		FROM `tabFrepple Manufacturing Order`
		""",
	as_dict=1)
		
	for mo in mos:
		print(mo)
		data = json.dumps({
			"reference": mo.latest_reference,
			# "operation": mo.operation,
			"status": mo.status,
			# "quantity": mo.quantity,
		})
		output = make_post_request(url,headers=headers, data=data)

def export_purchase_orders():
	api = "purchaseorder" #equivalent purchase order
	url,headers = get_frepple_params(api=api,filter=None)
	
	pos = frappe.db.sql(
		"""
		SELECT latest_reference,supplier,status
		FROM `tabFrepple Purchase Order`
		""",
	as_dict=1)
		
	for po in pos:
		print(po)
		data = json.dumps({
			"reference": po.latest_reference,
			# "supplier": po.supplier,
			"status": po.status,
		})
		output = make_post_request(url,headers=headers, data=data)



def import_manufacturing_order():
	api = "manufacturingorder"
	
	''' With filtering'''
	# filter = "?name=SAL-ORDER-0002"
	# filter = None
	# filter = "?status__contain=open"
	# url,headers = get_frepple_params(api=None,filter=filter)
	
	filter = "?status=proposed&operation_in=BOM"
	# filter = "?operation_in=BOM"
	
	url,headers = get_frepple_params(api=api,filter=filter)
	outputs = make_get_request(url,headers=headers)
	# print(type(outputs))
	# idx = 0
	# for output in outputs:
	# 	print(output["operation"])
	# 	print(output["operation"].split("@"))
	# 	if (len(output["operation"].split("@")) > 1): #routing type operation should only have 1 element, use this to filter out the routing type
	# 		print("Delete")
	# 		del outputs[idx]
	# 	idx = idx + 1

	# print(outputs)
	# Delete dictionary from list using list comprehension
	res = [output for output in outputs if not (len(output["operation"].split("@")) > 1)]

	return res

def generate_manufacturing_order(data):

	for i in data:
		# print(i["plan"])
		# idx = 0
		# demand = (list(i["plan"]["pegging"].keys())[idx])

		demands = (list(i["plan"]["pegging"].keys()))
		for demand in demands:
			mos = frappe.db.sql(
				"""
				SELECT name,demand
				FROM `tabFrepple Manufacturing Order`
				WHERE demand = %s
				""",
			demand,as_dict=1)
			print(mos)
			# if not frappe.db.exists("Frepple Manufacturing Order",i["reference"]):
			if not frappe.db.exists("Frepple Manufacturing Order",i["reference"]) and len(mos)== 0:
				#create new document
				new_doc = frappe.new_doc("Frepple Manufacturing Order")
				new_doc.reference = i["reference"]
				new_doc.latest_reference = i["reference"]
				new_doc.operation = i["operation"]
				new_doc.status = i["status"]
				new_doc.quantity = i["quantity"]
				new_doc.completed_quantity = i["quantity_completed"]
				new_doc.start_date = datetime.fromisoformat(i["startdate"])
				new_doc.end_date = datetime.fromisoformat(i["enddate"])
				new_doc.demand = demand
				new_doc.insert()
				print(new_doc.name)
			else:#update
				# if frappe.db.exists("Frepple Manufacturing Order",i["reference"]):
				existing_doc = frappe.get_doc("Frepple Manufacturing Order",mos[0].name)
				print(existing_doc)
				frappe.db.set_value('Frepple Manufacturing Order', mos[0].name, #Update the status
				{
					'latest_reference': i["reference"],
					'operation': i["operation"],
					'status': i["status"],
					'quantity': i["quantity"],
					# 'completed_quantity': i["quantity_completed"],
					'start_date': datetime.fromisoformat(i["startdate"]),
					'end_date': datetime.fromisoformat(i["enddate"])
				})
				# existing_doc.reference = i["reference"]
				# existing_doc.operation = i["operation"]
				# existing_doc.status = i["status"]
				# existing_doc.quantity = i["quantity"]
				# existing_doc.completed_quantity = i["quantity_completed"]
				# existing_doc.start_date = datetime.fromisoformat(i["startdate"])
				# existing_doc.end_date = datetime.fromisoformat(i["enddate"])
				# existing_doc.save(ignore_permissions=True, ignore_version=True)
				# existing_doc.reload()


def import_purchase_order():
	api = "purchaseorder"
	
	''' With filtering'''
	# filter = "?name=SAL-ORDER-0002"
	# filter = None
	# filter = "?status__contain=open"
	# url,headers = get_frepple_params(api=None,filter=filter)
	
	filter = "?status=proposed"
	
	url,headers = get_frepple_params(api=api,filter=filter)
	output = make_get_request(url,headers=headers)

	return output

def generate_purchase_order(data):

	for i in data:
		pos = frappe.db.sql(
			"""
			SELECT name,item,supplier
			FROM `tabFrepple Purchase Order`
			WHERE item = %s and supplier = %s
			""",
		[i["item"],i["supplier"]],as_dict=1)
		print (pos)
		if len(pos) == 0:
		# if not frappe.db.exists("Frepple Purchase Order",i["reference"]):
			new_doc = frappe.new_doc("Frepple Purchase Order")
			new_doc.reference = i["reference"]
			new_doc.latest_reference = i["reference"]
			new_doc.supplier = i["supplier"]
			new_doc.status = i["status"]
			new_doc.ordering_date = datetime.fromisoformat(i["startdate"])
			new_doc.receive_date =  datetime.fromisoformat(i["enddate"])
			new_doc.item = i["item"]
			new_doc.quantity =i["quantity"]
			new_doc.insert()
			print(new_doc.name)
		else: #update
			existing_doc = frappe.get_doc("Frepple Purchase Order",pos[0].name)
			frappe.db.set_value('Frepple Purchase Order', pos[0].name, #Update the status
			{
				'latest_reference': i["reference"],
				"ordering_date" : datetime.fromisoformat(i["startdate"]),
				"receive_date" :  datetime.fromisoformat(i["enddate"]),
				"quantity" : i["quantity"]
			})



