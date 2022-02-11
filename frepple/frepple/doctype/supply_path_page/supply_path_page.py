# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt
# '%@mzit!i8b*$zc&6oev96=Sat Jan 22 13:48:30 UTC 2022'

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import jwt
import time

class SupplyPathPage(Document):
	pass

@frappe.whitelist()
def get_iframe_url():
	doc = frappe.get_doc('Supply Path Page')
	doc_2 = frappe.get_doc('Frepple Settings')
	

	demand_to_show = ""
	if doc.demand:
		demand_to_show = doc.demand
	else:
		demands = frappe.db.get_list('Frepple Demand')
		demand_to_show = demands[0].name

	WEBTOKEN = jwt.encode({
		'exp': round(time.time()) + doc.expiration,    # Validity of the token
		'user': doc.user,                   	# User name
		'navbar': True if doc.show_navigation_bar else False                     # Whether or not frePPLe should render its navigation bar or not
	},
	doc_2.secret_key, # The shared secret between frePPLe and your application
	algorithm='HS256'
	).decode('ascii')

	print(doc.url + demand_to_show +'/?webtoken=' + WEBTOKEN)
	return doc.url + demand_to_show +'/?webtoken=' + WEBTOKEN