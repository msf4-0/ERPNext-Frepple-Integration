# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FreppleOperationResource(Document):
	pass


@frappe.whitelist()
def add_default_employee():
	frepple_resource = frappe.db.get_list('Frepple Resource',
		filters={
			'employee_check': 1,
		},
	)
	return frepple_resource[0].name