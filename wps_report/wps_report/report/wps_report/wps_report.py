# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime
from frappe.utils import getdate, flt

def execute(filters=None):
	# filters = frappe._dict(filters or {})
	if not filters: filters = {}
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": _("Record Type"),
			"fieldtype": "Data",
			"fieldname": "row_type",
			"width": 50

		},
		{
			"label": _("Employee Unique Id"),
			"fieldtype": "Data",
			"fieldname": "emp_no",
			"width": 150
		},
		{
			"label": _("Agent ID"),
			"fieldtype": "Data",
			"fieldname": "agent_id",
			"options": "",
			"width": 150
		},
		{
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"fieldname": "employee_name",
			"options": "",
			"width": 150
		},

		{
			"label": _("Employee Acc No"),
			"fieldtype": "Data",
			"fieldname": "emp_acc_no",
			"width": 180
		},
		{
			"label": _("Pay Start Date"),
			"fieldtype": "Data",
			"fieldname": "pay_start_date",
			"width": 100
		},
		{
			"label": _("Pay End Date"),
			"fieldtype": "Data",
			"fieldname": "pay_end_date",
			"width": 100
		},
		{
			"label": _("Days In Period"),
			"fieldtype": "Data",
			"fieldname": "pay_days",
			"width": 100
		},
		{
			"label": _("Fixed Income Amount"),
			"fieldtype": "Data",
			"fieldname": "fixed_income_amount",
			"width": 150
		},
		{
			"label": _("Variable Income Amount"),
			"fieldtype": "Data",
			"fieldname": "variable_income_amount",
			"width": 170
		},
		{
			"label": _("LWP"),
			"fieldtype": "Data",
			"fieldname": "lwp",
			"width": 150
		},
		{
			"label": _("Housing Allowance"),
			"fieldtype": "Data",
			"fieldname": "housing_allowance",
			"width": 150

		},
		{
			"label": _("Conveyance Allowance"),
			"fieldtype": "Data",
			"fieldname": "conveyance_allowance",
			"width": 150

		},
		{
			"label": _("Medical Allowance"),
			"fieldtype": "Data",
			"fieldname": "medical_allowance",
			"width": 150

		},
		{
			"label": _("Annual Passage Allowance"),
			"fieldtype": "Data",
			"fieldname": "annual_passage_allowance",
			"width": 150

		},
		{
			"label": _("Overtime Allowance"),
			"fieldtype": "Data",
			"fieldname": "overtime_allowance",
			"width": 150
		},
		{
			"label": _("Other Allowance"),
			"fieldtype": "Data",
			"fieldname": "other_allowance",
			"width": 150
		},
		{
			"label": _("Leave Encashment"),
			"fieldtype": "Data",
			"fieldname": "leave_encashment",
			"width": 150
		},

	]

	return columns

def get_conditions(filters):
	conditions = ""
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

	if filters.get("docstatus"):
		conditions += "tss.docstatus = {0}".format(doc_status[filters.get("docstatus")])

	if filters.get("from_date"): conditions += " and tss.start_date >= '{0}'".format(filters.get("from_date"))
	if filters.get("to_date"): conditions += " and tss.end_date <= '{0}'".format(filters.get("to_date"))

	return conditions, filters

def get_data(filters):

	data = []

	conditions, filters = get_conditions(filters)

	sql = """select
				'EDR' as type,
				(select
					te.wps_no
				from
					tabEmployee te
				where
					te.name = tss.employee) as wps_no,
				'AGENT ID' as lcc_code,
				(select
					te.lcc_code
				from
					tabEmployee te
				where
					te.name = tss.employee) as lcc_code,
				(select
					te.employee_name
				from
					tabEmployee te
				where
					te.name = tss.employee) as employee_name,
					
				(select
					te.iban_no
				from
					tabEmployee te
				where
					te.name = tss.employee) as iban_no,
				tss.start_date,
				tss.end_date,
				tss.total_working_days,
				tss.net_pay,
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Variable Income"
						and tsd.parentfield like "%earnings%"	) as sum_component,
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Fixed Income"
						and tsc2.salary_component = "Housing Allowance"
						and tsd.parentfield like "%earnings%"	) as component_one,	
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Fixed Income"
						and tsc2.salary_component =  "Conveyance Allowance"
						and tsd.parentfield like "%earnings%"	) as component_two,	
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Fixed Income"
						and tsc2.salary_component =  "Medical Allowance"
						and tsd.parentfield like "%earnings%"	) as component_three,	
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Fixed Income"
						and tsc2.salary_component =  "Annual Passage Allowance"
						and tsd.parentfield like "%earnings%"	) as component_four,
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Fixed Income"
						and tsc2.salary_component =  "Overtime Allowance"
						and tsd.parentfield like "%earnings%"	) as component_five,
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Fixed Income"
						and tsc2.salary_component =  "Other Allowance"
						and tsd.parentfield like "%earnings%"	) as component_six,	
				(select
						sum(tsd.amount)
					from
						`tabSalary Detail` tsd
						inner join `tabSalary Component` tsc2 on 
							tsd.salary_component = tsc2.name
					where
						tsd.parent = tss.name
						and tsc2.income_type = "Fixed Income"
						and tsc2.salary_component =  "Leave Encashment"
						and tsd.parentfield like "%earnings%"	) as component_seven,										
				tss.leave_without_pay
			from
				`tabPayroll Entry` tpe
			inner join `tabSalary Slip` tss on
				tss.payroll_entry = tpe.name
			where
				{}
			order by
				tss.creation desc""".format(conditions)

	# frappe.msgprint(sql)
	last_payroll = frappe.db.sql(sql, as_dict=True)
	employer_unique_id = frappe.db.get_single_value('WPS Default', 'employer_unique_id')
	employer_bank_code = frappe.db.get_single_value('WPS Default', 'employer_bank_code')
	employer_ref_no = frappe.db.get_single_value('WPS Default', 'employer_reference_no')

	total_amount = 0
	for d in last_payroll:
			total_amount = total_amount + d.net_pay
			row = {
				"row_type": d.type, "emp_no": d.wps_no, "agent_id": (d.lcc_code), "employee_name": d.employee_name,
				"emp_acc_no": (d.iban_no), "pay_start_date": d.start_date, "pay_end_date": d.end_date,
				"pay_days": d.total_working_days, "fixed_income_amount": d.net_pay, "variable_income_amount": d.sum_component, "housing_allowance": d.component_one, "coveyance_allowance": d.component_two, "medical_allowance" :d.component_three, "annual_passage_allowance" :d.component_four, "overtime_allowance" :d.component_five,"other_allowance" :d.component_six, "leave_enacashment" :d.component_seven,
				"lwp": d.leave_without_pay
				}
			data.append(row)
	row = {
		"row_type": 'SCR', "emp_no": employer_unique_id, "agent_id": employer_bank_code,
		"emp_acc_no": datetime.today().date(), "pay_start_date": datetime.strftime(datetime.today(),"%H%M"), "pay_end_date": datetime.strftime(datetime.strptime(filters.get("from_date"), "%Y-%m-%d"),"%m%Y"),
		"pay_days": len(last_payroll), "fixed_income_amount": flt(total_amount,3), "variable_income_amount": 'AED', "lwp": str(employer_ref_no)
	}
	data.append(row)
	return data