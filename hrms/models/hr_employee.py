# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta, date
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Hr Employee Inherit'

    @api.depends('from_current_leave_date', 'to_current_leave_date',
                 'from_last_leave_date', 'to_last_leave_date',
                 'from_upcoming_leave_date', 'to_upcoming_leave_date')
    def _compute_days(self):
        for record in self:
            record.total_current_days = self._calculate_days(record.from_current_leave_date,
                                                             record.to_current_leave_date)
            record.total_last_days = self._calculate_days(record.from_last_leave_date,
                                                          record.to_last_leave_date)
            record.total_upcoming_days = self._calculate_days(record.from_upcoming_leave_date,
                                                              record.to_upcoming_leave_date)

    def _calculate_days(self, start_date, end_date):
        if start_date and end_date:
            delta = fields.Date.from_string(end_date) - fields.Date.from_string(start_date)
            return delta.days + 1  # Include both start and end dates
        return 0

    age = fields.Integer("Age")
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

    # business_visa_exp_date = fields.Date(string="Business Visa Exp. Date")
    special_pass_exp_date = fields.Date(string="Special Pass Exp. Date")

    passport = fields.Binary(string="Passport")
    passport_file_name = fields.Char()
    passport_exp_date = fields.Date(string="Passport Expire Date")
    passport_taken_date = fields.Date(string="Passport Taken Date")
    passport_collect_date = fields.Date(string="Passport Collect Date")

    from_current_leave_date = fields.Date(string="From Current Leave Date")
    to_current_leave_date = fields.Date(string="To Current Leave Date")
    total_current_days = fields.Integer("Total Current Days", compute="_compute_days", store=True)

    from_last_leave_date = fields.Date(string="From Last Leave Date")
    to_last_leave_date = fields.Date(string="To Last Leave Date")
    total_last_days = fields.Integer("Total Last Days", compute="_compute_days", store=True)

    from_upcoming_leave_date = fields.Date(string="From Upcoming Leave Date")
    to_upcoming_leave_date = fields.Date(string="To Upcoming Leave Date")
    total_upcoming_days = fields.Integer("Total Upcoming Days", compute="_compute_days", store=True)

    remarks = fields.Text("Remarks")
    appraisal_last_date = fields.Date(string="Appraisal last Date")
    appraisal_last_amount = fields.Float(string="Appraisal Last Amount")

    offer_letter = fields.Binary("Offer Letter")
    offer_letter_file_name = fields.Char()
    government_contract_file = fields.Binary("Government Contract File")
    government_contract_file_name = fields.Char()
    experience_letter = fields.Binary("Experience Letter")
    experience_letter_file_name = fields.Char()

    permit_position = fields.Char("Permit Position")
    community = fields.Selection([('HINDU', 'HINDU'), ('MUSLIM', 'MUSLIM'), ('BOHRA', 'BOHRA'),
                                  ('SIKH', 'SIKH'), ('CHRISTIAN', 'CHRISTIAN'), ('Other', 'Other')], string="Community")
    job_description = fields.Text("Job Description")
    job_description_file = fields.Binary(string="Job Description File")
    job_description_file_name = fields.Char()

    letter_of_introduction_file = fields.Binary(string="Letter of Introduction")
    letter_of_introduction_file_name = fields.Char()

    guarantee_letter_file = fields.Binary(string="Guarantee Letter")
    guarantee_letter_file_name = fields.Char()

    salary_hr_note = fields.Text("Hr Note")
    salary_admin_note = fields.Text("Admin Note")

    # Define the total fields
    total_in_hand_allowance = fields.Monetary(string='Total In Hand Allowance', compute='_compute_total_allowances', store=True)
    total_other_allowance = fields.Monetary(string='Total Other Allowance', compute='_compute_total_allowances', store=True)
    total_ctc = fields.Monetary(string='Total CTC', compute='_compute_total_ctc', store=True)

    bank_details_line_ids = fields.One2many('res.partner.bank', 'employee_id',
                                            string="Bank Details Lines")
    education_detail_line_ids = fields.One2many('hr.education.details', 'employee_id',
                                                string="Education Details Lines")
    compensation_detail_line_ids = fields.One2many('hr.compensation.details', 'employee_id',
                                                   string="Compensation Details Lines")
    salary_detail_line_ids = fields.One2many('hr.salary.details', 'employee_id',
                                             string="Salary Details Lines")
    employee_lang_ids = fields.Many2many('res.lang', string="Language Known")
    date_of_joining = fields.Date("Date of Joining")

    @api.onchange('has_work_permit')
    def _onchange_has_work_permit(self):
        return self._check_file_size('has_work_permit', 'Work Permit')

    @api.onchange('pan_no')
    def _onchange_pan_no(self):
        return self._check_file_size('pan_no', 'PAN Card No.')

    @api.onchange('aadhaar_no')
    def _onchange_aadhaar_no(self):
        return self._check_file_size('aadhaar_no', 'Aadhaar Card No.')

    @api.onchange('medical_certificate')
    def _onchange_medical_certificate(self):
        return self._check_file_size('medical_certificate', 'Medical Certificate')

    @api.onchange('pcc_certificate')
    def _onchange_pcc_certificate(self):
        return self._check_file_size('pcc_certificate', 'PCC Certificate')

    @api.onchange('passport')
    def _onchange_passport(self):
        return self._check_file_size('passport', 'Passport')

    @api.onchange('offer_letter')
    def _onchange_offer_letter(self):
        return self._check_file_size('offer_letter', 'Offer Letter')

    @api.onchange('government_contract_file')
    def _onchange_government_contract_file(self):
        return self._check_file_size('government_contract_file', 'Government Contract File')

    @api.onchange('experience_letter')
    def _onchange_experience_letter(self):
        return self._check_file_size('experience_letter', 'Experience Letter')

    @api.onchange('job_description_file')
    def _onchange_job_description_file(self):
        return self._check_file_size('job_description_file', 'Job Description File')

    def _check_file_size(self, field_name, field_label):
        file_content = getattr(self, field_name)
        if file_content:
            file_size = len(file_content)
            if file_size > 1024 * 1024:
                setattr(self, field_name, False)
                return {
                    'warning': {
                        'title': "File Size Exceeded",
                        'message': f"File size cannot exceed 1024 KB (1 MB)."
                                   f" Please upload a smaller file for {field_label}.",
                    }
                }

    @api.onchange('from_current_leave_date', 'to_current_leave_date',
                  'from_last_leave_date', 'to_last_leave_date',
                  'from_upcoming_leave_date', 'to_upcoming_leave_date')
    def _onchange_leave_dates(self):
        today = date.today()
        for record in self:
            for leave_type in [
                ('from_current_leave_date', 'to_current_leave_date', "Current Leave"),
                # ('from_last_leave_date', 'to_last_leave_date', "Last Leave"),
                ('from_upcoming_leave_date', 'to_upcoming_leave_date', "Upcoming Leave"),
            ]:
                from_date = getattr(record, leave_type[0])
                to_date = getattr(record, leave_type[1])
                if from_date and to_date:
                    if from_date > to_date:
                        return {
                            'warning': {
                                'title': "Invalid Date Range",
                                'message': f"The 'From {leave_type[2]} Date' must be earlier than the 'To {leave_type[2]} Date'.",
                            }
                        }
                if from_date and from_date < today:
                    return {
                        'warning': {
                            'title': "Invalid Date",
                            'message': f"The 'From {leave_type[2]} Date' must be in the future.",
                        }
                    }
                if to_date and to_date < today:
                    return {
                        'warning': {
                            'title': "Invalid Date",
                            'message': f"The 'To {leave_type[2]} Date' must be in the future.",
                        }
                    }

    @api.depends('salary_detail_line_ids.amount', 'salary_detail_line_ids.salary_type')
    def _compute_total_allowances(self):
        for record in self:
            total_in_hand = 0.0
            total_other = 0.0
            for line in record.salary_detail_line_ids:
                if line.salary_type == 'in_hand':
                    total_in_hand += line.amount
                elif line.salary_type == 'others':
                    total_other += line.amount
            record.total_in_hand_allowance = total_in_hand
            record.total_other_allowance = total_other

    @api.depends('total_in_hand_allowance', 'total_other_allowance')
    def _compute_total_ctc(self):
        for record in self:
            record.total_ctc = record.total_in_hand_allowance + record.total_other_allowance

    @api.model
    def default_get(self, fields):
        res = super(HrEmployee, self).default_get(fields)

        # Load salary details from the salary.master
        salary_master_records = self.env['salary.master'].search([])
        salary_details = []

        for record in salary_master_records:
            salary_details.append((0, 0, {
                'component_id': record.id,
                'salary_type': record.salary_type,
                'amount': 0.0,
                'currency_id': res.get('currency_id'),
                'remarks': '',
            }))

        res['salary_detail_line_ids'] = salary_details
        return res

    def write(self, vals):
        result = super(HrEmployee, self).write(vals)

        for employee in self:
            if not employee.salary_detail_line_ids:
                salary_master_records = self.env['salary.master'].search([])
                salary_details = []

                for record in salary_master_records:
                    salary_details.append((0, 0, {
                        'employee_id': employee.id,
                        'component_id': record.id,
                        'salary_type': record.salary_type,
                        'amount': 0.0,
                        'currency_id': employee.currency_id.id,
                        'remarks': '',
                    }))

                if salary_details:
                    employee.write({'salary_detail_line_ids': salary_details})

        return result

    def action_populate_salary_details(self):
        for employee in self:
            # Get existing salary component IDs
            existing_components = employee.salary_detail_line_ids.mapped('component_id.id')

            # Get all salary master records
            salary_master_records = self.env['salary.master'].search([])

            # Create new salary details for missing components
            salary_details = [
                (0, 0, {
                    'employee_id': employee.id,
                    'component_id': record.id,
                    'salary_type': record.salary_type,
                    'amount': 0.0,
                    'currency_id': employee.currency_id.id,
                    'remarks': '',
                })
                for record in salary_master_records
                if record.id not in existing_components
            ]

            # Write new salary details if there are any
            if salary_details:
                employee.write({'salary_detail_line_ids': [(0, 0, detail[2]) for detail in salary_details]})

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Salary details populated for this employees with blank salary details.',
                'sticky': False,
            },
        }

    @api.model
    def _cron_send_visa_expiration_reminders(self):
        today = fields.Date.today()
        ninty_days_later = today + timedelta(days=90)

        # Find employees with visa expiring within the next 3 months
        employees = self.search([
            ('visa_expire', '>=', today),
            ('visa_expire', '<=', ninty_days_later)
        ])

        for employee in employees:
            template_id = self.env.ref('hrms.email_template_visa_reminder')
            if template_id:
                email_values = {
                    'email_from': 'hr@africab.com',
                    'email_to': 'qutub@africab.co.tz,shabbir@africab.co.tz',
                    'email_cc': employee.work_email
                }
                template_id.send_mail(employee.id, email_values=email_values, force_send=True)

    @api.model
    def _cron_send_passport_expiration_reminders(self):
        today = fields.Date.today()
        six_month_later = today + timedelta(days=180)

        # Find employees with passport expiring within the next 6 months
        employees = self.search([
            ('passport_exp_date', '>=', today),
            ('passport_exp_date', '<=', six_month_later)
        ])

        for employee in employees:
            template_id = self.env.ref('hrms.email_template_passport_reminder')
            if template_id:
                email_values = {
                    'email_from': 'hr@africab.com',
                    'email_to': 'qutub@africab.co.tz,shabbir@africab.co.tz',
                    'email_cc': employee.work_email
                }
                template_id.send_mail(employee.id, email_values=email_values, force_send=True)

    @api.model
    def _cron_send_passport_collect_date_expiration_reminders(self):
        today = fields.Date.today()
        two_days_ago = today - timedelta(days=2)

        # Find employees with expired passport collect dates and no reminder sent
        employees = self.search([
            ('passport_collect_date', '<', two_days_ago)
        ])

        for employee in employees:
            template_id = self.env.ref('hrms.email_template_passport_collect_date_expiration_reminder')
            if template_id:
                email_values = {
                    'email_from': 'hr@africab.com',
                    'email_to': employee.work_email,
                    'email_cc': 'qutub@africab.co.tz,shabbir@africab.co.tz,taher.bhandari@africab.co.tz',
                }
                template_id.send_mail(employee.id, email_values=email_values, force_send=True)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    branch_name = fields.Char("Branch Name")
    ifsc_code = fields.Char(related='bank_id.bic', readonly=False)


class ResumeLine(models.Model):
    _inherit = 'hr.resume.line'
    _description = "Resume line of an employee inherit"

    resume = fields.Binary("Resume")
    resume_file_name = fields.Char()

    @api.onchange('resume')
    def _onchange_resume(self):
        return self._check_file_size('resume', 'Resume')

    def _check_file_size(self, field_name, field_label):
        file_content = getattr(self, field_name)
        if file_content:
            file_size = len(file_content)
            if file_size > 1024 * 1024:
                setattr(self, field_name, False)
                return {
                    'warning': {
                        'title': "File Size Exceeded",
                        'message': f"File size cannot exceed 1024 KB (1 MB)."
                                   f" Please upload a smaller file for {field_label}.",
                    }
                }


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

    @api.onchange('degree')
    def _onchange_degree(self):
        return self._check_file_size('degree', 'Degree')

    def _check_file_size(self, field_name, field_label):
        file_content = getattr(self, field_name)
        if file_content:
            file_size = len(file_content)
            if file_size > 1024 * 1024:
                setattr(self, field_name, False)
                return {
                    'warning': {
                        'title': "File Size Exceeded",
                        'message': f"File size cannot exceed 1024 KB (1 MB)."
                                   f" Please upload a smaller file for {field_label}.",
                    }
                }


class CompensationDetails(models.Model):
    _name = 'hr.compensation.details'
    _description = "Employee compensation details"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    name = fields.Char(string="Component")
    amount = fields.Float(string="Amount")
    currency_id = fields.Many2one('res.currency', string="Currency")


class HrSalaryDetails(models.Model):
    _name = 'hr.salary.details'
    _description = "Employee salary compensation details"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    component_id = fields.Many2one('salary.master', string="Component")
    salary_type = fields.Selection([('in_hand', 'In-hand'), ('others', 'Others')],
                                   string="Salary Type")
    amount = fields.Float(string="Amount")
    currency_id = fields.Many2one('res.currency', string="Currency")
    remarks = fields.Text("Remarks")
