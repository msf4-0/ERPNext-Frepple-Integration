# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,json
from frappe.model.document import Document

class FreppleIntegrationDataFetching(Document):
	pass

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

def fetch_locations():
	locations = frappe.db.sql("""SELECT name FROM `tabWarehouse`""",as_dict=1)
	for location in locations:
		if not frappe.db.exists("Frepple Location",location.name):
			new_location = frappe.new_doc("Frepple Location")
			new_location.warehouse = location.name
			new_location.insert()

@frappe.whitelist()
def fetch_data(doc):
	doc = json.loads(doc)
	if doc["frepple_item"]:
		fetch_items()
	if doc["frepple_customer"]:
		fetch_customers()
	if doc["frepple_location"]:
		fetch_locations()
	