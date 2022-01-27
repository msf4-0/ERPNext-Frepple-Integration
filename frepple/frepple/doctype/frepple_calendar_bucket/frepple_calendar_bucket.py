# -*- coding: utf-8 -*-
# Copyright (c) 2022, Drayang Chua and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class FreppleCalendarBucket(Document):
	
	@frappe.whitelist()
	def add_to_calendar(self):
		if(self.calendar):
			doc= frappe.get_doc("Frepple Calendar",self.calendar)
	
	#	Need to add a condition check to prevent adding duplicate row 

			
			# calendar_bucket_list = doc.calendar_bucket
			# for row in calendar_bucket_list
			row = doc.append("calendar_bucket",{})
			row.calendar_bucket = self.name
			row.start_datetime=self.start_datetime
			row.end_datetime = self.end_datetime
			row.start_time = self.start_time
			row.end_time = self.end_time
			row.monday = self.monday
			row.tuesday = self.tuesday
			row.wednesday = self.wednesday
			row.thursday = self.thursday
			row.friday = self.friday
			row.saturday = self.saturday
			row.sunday = self.sunday

			# frappe.msgprint(
			# 	msg='{}.',
			# 	title='Note',
			# )

			frappe.msgprint(_("{0} calendar is updated.").format(self.calendar))

			row.save(ignore_permissions=True, ignore_version=True)
			row.reload()