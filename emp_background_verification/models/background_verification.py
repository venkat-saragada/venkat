# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo import exceptions
from odoo.exceptions import ValidationError, Warning, UserError,except_orm
from odoo.tools.translate import _
import time
from custom_functions import check_file_format
import re

class ReferralCategory(models.Model):
	_name = 'referral_category.referral_category'
	_rec_name = 'referral_category_name'
	_sql_constraints = [('category_name_uniq', 'unique(referral_category_name)', 'Category already exists..!')]

	referral_category_name = fields.Char(string="Referral Category Name", )


class reference_check_list(models.Model):
	_name = 'referral_check_list.referral_check_list'
	_rec_name = 'referral_checklist_name'
	_sql_constraints = [('checklist_name_uniq', 'unique(referral_checklist_name, country_id)', 'Checklist Name already exists for this Country..!')]

	referral_checklist_name = fields.Char(string="Referral Checklist Name",)
	# referral_category = fields.Many2one('referral_category.referral_category',string ="Referral Category",)
	referral_category = fields.Selection([('address', 'Address'),('academics', 'Academics'),('employment', 'Employment')])
	country_id = fields.Many2one('res.country', string='Country')


class emp_background_verification(models.Model):
	_name = 'emp_verification.emp_verification'
	_rec_name = 'user_id'
	_inherit = ['mail.thread']
	_sql_constraints = [('user_id_uniq', 'unique(user_id)', 'Record for this User already exists..!')]

	user_id = fields.Many2one('res.users',string="User Id", default=lambda self: self.env.uid,)
	# employee_id = fields.Many2one('hr.employee',string="Employee Name", default=lambda self: self.env.uid, )
	# Checklist
	address_check = fields.Boolean(string="Address",)
	academic_check = fields.Boolean(string="Academics",)
	employment_check = fields.Boolean(string="Is Experienced?")
	passport_check = fields.Boolean(string="Have Passport?")
	# Address fields
	address_checklist = fields.Many2one('referral_check_list.referral_check_list', string="Address Checklist")
	name_as_per_proof = fields.Char(string="Name as per Proof")
	address_line = fields.Text(string="Full Address")
	city_town = fields.Char(string="City / Town")
	state_province = fields.Char(string="State / Province")
	zip_code = fields.Char(string ="Zip Code")
	country_id = fields.Many2one('res.country', string="Country")
	address_proof_id = fields.Char(string="Address Proof No.")
	address_proof = fields.Binary(string="Address Proof")
	address_file = fields.Char(string="Address Proof File")
	# Academic fields
	academic_details_id = fields.One2many(comodel_name='academic.details', inverse_name='parent_id', string='Academic Details')
	# Employment fields
	employment_details_id = fields.One2many(comodel_name='employment.details', inverse_name='parent_id', string='Employment History',)
	# Passport fields
	name_as_per_passport = fields.Char(string="Name as per Passport")
	passport_number = fields.Char(string="Passport No.")
	passport_issue_date = fields.Date(string="Date of Issue")
	passport_expiry_date = fields.Date(string="Date of Expiry")
	place_of_issue = fields.Char(string="Place of Issue")
	upload_passport = fields.Binary(string="Passport")
	passport_file = fields.Char(string="Passport File")
	# state = fields.Selection([('draft','Draft'),('waiting','Waiting'),('verified','Verified')], default='draft', string='Status')
	state = fields.Selection([('draft','Draft'),('waiting','Waiting'),('verified','Verified')], default='draft', string='Status',track_visibility='always')

 	@api.onchange('address_proof_id','passport_number')
	def on_change_address_proof_id_passport_no(self):
		if self.address_proof_id:
			self.address_proof_id = self.address_proof_id.upper()
		if self.passport_number:
			self.passport_number = self.passport_number.upper()

	@api.onchange('address_file')
	def on_change_address_file(self):
		if self.address_file:
			if check_file_format(self.address_file):
				raise Warning('Upload file in pdf format only...!')

	@api.onchange('passport_file')
	def on_change_passport_file(self):
		if self.passport_file:
			if check_file_format(self.passport_file):
				raise Warning('Upload file in pdf format only...!')

	@api.onchange('passport_issue_date','passport_expiry_date')
	def on_change_passport_expiry_date(self):
		if self.passport_issue_date and self.passport_expiry_date:
			if self.passport_expiry_date <= self.passport_issue_date:
				warning_msg = {
					'values': {'self.passport_expiry_date':self.passport_issue_date},
					'warning': {
						'title': 'Validation Error',
						'message': 'Expiry Date can not be before or same as Issue Date'
					}
				}
				return warning_msg

	@api.one
	def submit(self):
		for rec in self:
			if rec.address_check and rec.academic_check and rec.employment_check and rec.passport_check:
				if rec.address_proof_id and rec.academic_details_id and rec.employment_details_id and rec.passport_number:
					self.state = 'waiting'
				else:
					if not rec.academic_details_id:
						raise Warning('Fill Academic details..!')
					elif not rec.employment_details_id :
						raise Warning('Fill Employment details..!')
			elif rec.address_check and rec.academic_check and rec.employment_check:
				if rec.address_proof_id and rec.academic_details_id and rec.employment_details_id:
					self.state = 'waiting'
				else:
					if not rec.academic_details_id:
						raise Warning('Fill Academic details..!')
					elif not rec.employment_details_id :
						raise Warning('Fill Employment details..!')
			elif rec.address_check and rec.academic_check and rec.passport_check:
				if rec.address_proof_id and rec.academic_details_id and rec.passport_number:
					self.state = 'waiting'
				else:
					if not rec.academic_details_id:
						raise Warning('Fill Academic details..!')
			elif rec.address_check and rec.academic_check:
				if rec.address_proof_id and rec.academic_details_id:
					self.state = 'waiting'
				else:
					if not rec.academic_details_id:
						raise Warning('Fill Academic details..!')

	@api.one
	def refuse(self):
		self.state='draft'

	@api.one
	def verify(self):
		self.state='verified'


class AcademicDetails(models.Model):
	_name = 'academic.details'
	_sql_constraints = [('academic_checklist_uniq', 'unique(qualification_checklist, parent_id)', 'Duplicate Qualification Records not allowed..!')]

	parent_id = fields.Many2one('emp_verification.emp_verification', string='Academic Details Id')
	qualification_checklist = fields.Many2one('referral_check_list.referral_check_list', string="Qualification")
	roll_no = fields.Char(string="Roll Number",)
	degree = fields.Char(string="Degree")
	specialization = fields.Char(string="Specialization")
	institution_name = fields.Char(string="Institution")
	university = fields.Char(string="Board / University")
	year_of_passing = fields.Date(string="Year of Passing")
	percentage = fields.Float(string="Percentage / CGPA")
	upload_marks_sheet = fields.Binary(string="Marks Sheet")
	marks_sheet_file = fields.Char(string="Marks Sheet File")

	@api.onchange('marks_sheet_file')
	def on_change_marks_sheet_file(self):
		if self.marks_sheet_file:
			if check_file_format(self.marks_sheet_file):
				raise Warning('Upload file in pdf format only...!')

	@api.onchange('percentage')
	def on_change_percentage(self):
		for rec in self:
			if rec.percentage:
				if not rec.percentage > 0.00:
					raise Warning('Invalid Percentage / CGPA')


class EmploymentDetails(models.Model):
	_name = 'employment.details'
	_sql_constraints = [('employment_checklist_uniq', 'unique(employment_checklist, parent_id)', 'Duplicate Employer Records not allowed..!')]

	parent_id = fields.Many2one('emp_verification.emp_verification', string='Employment History Id')
	employment_checklist = fields.Many2one('referral_check_list.referral_check_list', string="Employer")
	company_name = fields.Char(string="Company Name")
	company_address = fields.Text(string="Company Address")
	emp_id = fields.Char(string="Employee Id")
	designation = fields.Char(string="Designation")
	emp_department = fields.Char(string="Department")
	cost_to_company = fields.Float(string="Cost to Company")
	joining_date = fields.Date(string="Date of Joining")
	relieving_date = fields.Date(string="Date of Relieving")
	resignation_reason = fields.Text(string="Reason for Resignation")
	upload_relieving_letter = fields.Binary(string="Relieving Letter")
	relieving_file = fields.Char(string="Relieving File",)
	upload_payslip = fields.Binary(string="Payslip")
	payslip_file = fields.Char(string="Payslip File")
	hr_name = fields.Char(string="HR Name")
	hr_email = fields.Char(string="HR Email Id")

	@api.onchange('relieving_file')
	def on_change_relieving_file(self):
		if self.relieving_file:
			if check_file_format(self.relieving_file):
				raise Warning('Upload file in pdf format only...!')
	
	@api.onchange('payslip_file')
	def on_change_payslip_file(self):
		if self.payslip_file:
			if check_file_format(self.payslip_file):
				raise Warning('Upload file in pdf format only...!')
 	
 	@api.onchange('hr_email')
 	def on_change_hr_email(self):
 		if self.hr_email:
 			email_val = self.hr_email
 			if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_val) != None:
 				self.hr_email = email_val
 			else:
 				# raise Warning('Please enter a valid email address')
 				raise except_orm("Please enter a valid email address")
 				# raise except_orm(_('Invalid Email'), _("Please enter a valid email address"))
 				self.hr_email = ''
