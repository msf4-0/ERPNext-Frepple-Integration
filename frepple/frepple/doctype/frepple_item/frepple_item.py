# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FreppleItem(Document):
	pass


# frappe.whitelist()
# def create_frepple_item(doc):
# 	doc = json.loads(doc) #dict form
# 	name = doc['item_owner']

# 	doc = frappe.new_doc('Frepple Item')
# 	doc.item = 'Product'
# 	doc.insert()

# 	return name