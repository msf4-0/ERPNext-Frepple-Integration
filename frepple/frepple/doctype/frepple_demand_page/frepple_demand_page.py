# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt
# '%@mzit!i8b*$zc&6oev96=Sat Jan 22 13:48:30 UTC 2022'

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import jwt
import time

class FreppleDemandPage(Document):
	pass

@frappe.whitelist()
def get_iframe_url():
	doc = frappe.get_doc('Frepple Demand Page')
	doc_2 = frappe.get_doc('Frepple Settings')

	WEBTOKEN = jwt.encode({
		'exp': round(time.time()) + doc.expiration,    # Validity of the token
		'user': doc.user,                   	# User name
		'navbar': True if doc.show_navigation_bar else False                     # Whether or not frePPLe should render its navigation bar or not
	},   
	doc_2.secret_key, # The shared secret between frePPLe and your application
	algorithm='HS256'
	).decode('ascii')

	return doc.url + '?webtoken=' + WEBTOKEN