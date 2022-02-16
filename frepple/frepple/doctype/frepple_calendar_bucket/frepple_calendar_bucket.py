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
		exist = 0
		if(self.calendar):
			doc= frappe.get_doc("Frepple Calendar",self.calendar)
	
			
			calendar_buckets = frappe.db.sql(
				"""
				SELECT fc.name, fccb.calendar_bucket 
				FROM `tabFrepple Calendar` fc, `tabFrepple Calendar Calendar Bucket` fccb
				WHERE fc.name = fccb.parent
				""",
			as_dict=1)
			# condition check to prevent adding duplicate row 
			for calendar_bucket in calendar_buckets:
				print(calendar_bucket)
				if calendar_bucket.calendar_bucket == self.name:
					exist = 1


			if exist != 1: #if the calendar bucket is not added to the calendar before
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

				frappe.msgprint(_("{0} calendar is updated.").format(self.calendar))

				row.save(ignore_permissions=True, ignore_version=True)
				row.reload()
	
	@frappe.whitelist()
	def check_priority(self):
		duplicate = 0

		if(self.calendar):
			doc= frappe.get_doc("Frepple Calendar",self.calendar)
	
			
			calendar_buckets = frappe.db.sql(
				"""
				SELECT name, priority,calendar
				FROM `tabFrepple Calendar Bucket`
				WHERE calendar = %s
				""",
			doc.name,as_dict=1)

			for calendar_bucket in calendar_buckets:
				print(calendar_bucket)
				if self.priority == calendar_bucket.priority:
					duplicate = 1

		return duplicate