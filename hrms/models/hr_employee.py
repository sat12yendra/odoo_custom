# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Hr Employee Inherit'

    age = fields.Integer("Age")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')])
    nssf_no = fields.Char("NSSF No.")
    tin_no = fields.Char("Tin No.")
    whatsapp_no = fields.Char("WhatsApp No.")
    pan_no = fields.Binary(string="PAN Card No.")
    pan_no_file_name = fields.Char()
    aadhaar_no = fields.Binary(string="Aadhaar Card No.")
    aadhaar_no_file_name = fields.Char()
    alien_card = fields.Char(string="Alien Card")
    swift_code = fields.Char(string="Swift Code")
    medical_certificate = fields.Binary(string="Medical Certificate")
    pcc_certificate = fields.Binary(string="PCC Certificate")

    business_visa_exp_date = fields.Date(string="Business Visa Exp. Date")
    special_pass_exp_date = fields.Date(string="Special Pass Exp. Date")

    passport = fields.Binary(string="Passport")
    passport_file_name = fields.Char()
    passport_exp_date = fields.Date(string="Passport Expire Date")

    upcoming_leave_date = fields.Date(string="Upcoming Leave Date")
    last_leave_date = fields.Date(string="Last Leave Date")
    # package_salary = fields.Integer("Package (Salary)")
    remarks = fields.Text("Remarks")
    appraisal_last_date = fields.Date(string="Appraisal last Date")
    appraisal_last_amount = fields.Float(string="Appraisal Last Amount")

    offer_letter = fields.Binary("Offer Letter")
    offer_letter_file_name = fields.Char()
    experience_letter = fields.Binary("Experience Letter")
    experience_letter_file_name = fields.Char()

    bank_details_line_ids = fields.One2many('res.partner.bank', 'employee_id',
                                            string="Bank Details Lines")
    education_detail_line_ids = fields.One2many('hr.education.details', 'employee_id',
                                                string="Education Details Lines")
    compensation_detail_line_ids = fields.One2many('hr.compensation.details', 'employee_id',
                                                   string="Compensation Details Lines")

    @api.model
    def _cron_send_visa_expiration_reminders(self):
        today = fields.Date.today()
        thirty_days_later = today + timedelta(days=30)

        # Find employees with visa expiring within the next 30 days
        employees = self.search([
            ('business_visa_exp_date', '>=', today),
            ('business_visa_exp_date', '<=', thirty_days_later)
        ])

        for employee in employees:
            days_left = (employee.business_visa_exp_date - today).days
            template_id = self.env.ref('hrms.email_template_visa_reminder')
            if template_id:
                # Use with_context to pass additional variables to the email template
                template_id.with_context(days_left=days_left).send_mail(employee.id, force_send=True)

    @api.model
    def _cron_send_passport_expiration_reminders(self):
        today = fields.Date.today()
        thirty_days_later = today + timedelta(days=30)

        # Find employees with passport expiring within the next 30 days
        employees = self.search([
            ('passport_exp_date', '>=', today),
            ('passport_exp_date', '<=', thirty_days_later)
        ])

        for employee in employees:
            days_left = (employee.passport_exp_date - today).days
            template_id = self.env.ref('hrms.email_template_passport_reminder')
            if template_id:
                # Use with_context to pass additional variables to the email template
                template_id.with_context(days_left=days_left).send_mail(employee.id, force_send=True)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    branch_name = fields.Char("Branch Name")
    ifsc_code = fields.Char(related='bank_id.bic')


class ResumeLine(models.Model):
    _inherit = 'hr.resume.line'
    _description = "Resume line of an employee inherit"

    resume = fields.Binary("Resume")
    resume_file_name = fields.Char()


class EmployeeEducationDetails(models.Model):
    _name = 'hr.education.details'
    _description = "Resume line of an employee inherit"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], 'Certificate Level', default='other', groups="hr.group_hr_user")
    study_field = fields.Char("Field of Study", groups="hr.group_hr_user")
    study_school = fields.Char("School/Institution", groups="hr.group_hr_user")
    subject = fields.Char(string="Subject")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    degree = fields.Binary(string="Degree")
    degree_file_name = fields.Char()
    grade = fields.Char(string="Grade")
    percentage = fields.Float(string="Percentage")


class CompensationDetails(models.Model):
    _name = 'hr.compensation.details'
    _description = "Employee compensation details"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    name = fields.Char(string="Component")
    amount = fields.Float(string="Amount")
    currency_id = fields.Many2one('res.currency', string="Currency")
