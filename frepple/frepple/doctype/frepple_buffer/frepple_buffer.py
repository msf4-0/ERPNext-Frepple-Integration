# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document

class FreppleBuffer(Document):
	pass

# Sync the bin in erpnext with the buffer in frepple
@frappe.whitelist()
def update_frepple_buffer(doc):

	if (frappe.get_doc("Frepple Settings").frepple_integration):
	
		doc = json.loads(doc)
		bin = frappe.get_doc("Bin",doc["name"]) #ERPNext work order

		# Do condition check

		print(bin)
		buffers = frappe.db.sql(
			"""
			SELECT item,location,name
			FROM `tabFrepple Buffer`
			WHERE item = %s and location = %s
			""",
		[bin.item_code,bin.warehouse],as_dict=1)


		for buffer in buffers:
			frappe.db.set_value('Frepple Buffer', buffer.name, {
				'onhand':bin.actual_qty,
			}) #Update the quantity


