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

from frepple.frepple.doctype.frepple_data_export.frepple_data_export import get_frepple_params

class FreppleRunPlan(Document):
	pass

@frappe.whitelist()
def run_plan(doc):
	constraint= 0
	plantype = 1
	# filter = "/execute/api/runplan/?"
	doc = json.loads(doc)
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
		msg='Plan have been runned succesffully',
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


def import_manufacturing_order():
	api = "manufacturingorder"
	
	''' With filtering'''
	# filter = "?name=SAL-ORDER-0002"
	# filter = None
	# filter = "?status__contain=open"
	# url,headers = get_frepple_params(api=None,filter=filter)
	
	filter = "?operation_in=BOM-&status=proposed"
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
	print(type(res))
	return res

def generate_manufacturing_order(data):

	for i in data:
		if not frappe.db.exists("Frepple Manufacturing Order",i["reference"]):
			new_doc = frappe.new_doc("Frepple Manufacturing Order")
			new_doc.reference = i["reference"]
			new_doc.operation = i["operation"]
			new_doc.status = i["status"]
			new_doc.quantity = i["quantity"]
			new_doc.completed_quantity = i["quantity_completed"]
			new_doc.start_date = datetime.fromisoformat(i["startdate"])
			new_doc.end_date = datetime.fromisoformat(i["enddate"])
			new_doc.insert()
			print(new_doc.name)


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
		if not frappe.db.exists("Frepple Purchase Order",i["reference"]):
			new_doc = frappe.new_doc("Frepple Purchase Order")
			new_doc.reference = i["reference"]
			new_doc.supplier = i["supplier"]
			new_doc.status = i["status"]
			new_doc.ordering_date = datetime.fromisoformat(i["startdate"])
			new_doc.receive_date =  datetime.fromisoformat(i["enddate"])
			new_doc.item = i["item"]
			new_doc.quantity =i["quantity"]
			new_doc.insert()
			print(new_doc.name)

