# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import jwt
import time

class FreppleCustomPageSettings(Document):
	pass

@frappe.whitelist()
def get_iframe_url(pageName):
	doc = frappe.get_doc('Frepple Custom Page Settings', pageName)
	doc_2 = frappe.get_doc("Frepple Settings")

	WEBTOKEN = jwt.encode({
		'exp': round(time.time()) + doc.expiration,    # Validity of the token
		'user': doc.user,                   	# User name
		'navbar': True if doc.show_navigation_bar else False                     # Whether or not frePPLe should render its navigation bar or not
	},
	# doc.secret_key,    # The shared secret between frePPLe and your application
	doc_2.secret_key,
	algorithm='HS256'
	).decode('ascii')

	return {
		'iframeHeight': doc.iframe_height,
		'URL': doc.url + '?webtoken=' + WEBTOKEN
	}

@frappe.whitelist()
def get_secret_key():
	doc_2 = frappe.get_doc("Frepple Settings")

	return doc_2.secret_key