# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import jwt
import time

class FreppleTestPage(Document):
	pass

@frappe.whitelist()
def get_iframe_url():
	WEBTOKEN = jwt.encode({
		'exp': round(time.time()) + 600,    # Validity of the token
		'user': 'admin',                   	# User name
		'navbar': True                     # Whether or not frePPLe should render its navigation bar or not
	},
	'%@mzit!i8b*$zc&6oev96=Sat Jan 22 13:48:30 UTC 2022',    # The shared secret between frePPLe and your application
	algorithm='HS256'
	).decode('ascii')

	return WEBTOKEN