# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeWorkPerformance(models.Model):
    _name = 'employee.work.performance'
    _rec_name = "employee_id"
    _inherit = ['mail.thread']
    _description = 'Create Employee Work Performance'

    employee_id = fields.Many2one('hr.employee', string="Employee Name", tracking=True)
    department_id = fields.Many2one(related='employee_id.department_id', string='Department',
                                    check_company=True, tracking=True)
    company_id = fields.Many2one(related='employee_id.company_id', string='Company', tracking=True)
    job_id = fields.Many2one(related='employee_id.job_id', string='Job Position',
                             check_company=True, tracking=True)
    job_title = fields.Char(related='employee_id.job_title', string="Job Title",
                            readonly=True, tracking=True)
    permit_position = fields.Char(related='employee_id.permit_position', string="Permit Position",
                                  readonly=True, tracking=True)
    parent_id = fields.Many2one(related='employee_id.parent_id', string='Manager', tracking=True)
    date = fields.Date("Date", tracking=True)
    year_of_kpi = fields.Char("Year of KPI", readonly=True, tracking=True)
    employee_kpi_ids = fields.One2many('employee.kpi',
                                     'employee_work_performance_id', string="Employee KPI")
    employee_task_ids = fields.One2many('employee.task',
                                             'employee_work_performance_id', string="Employee behaviour")
    employee_behaviour_ids = fields.One2many('employee.behaviour',
                                     'employee_work_performance_id', string="Employee behaviour")
    employee_innovation_ids = fields.One2many('employee.innovation',
                                             'employee_work_performance_id', string="Employee behaviour")

    @api.onchange('date')
    def _onchange_date(self):
        if self.date:
            self.year_of_kpi = self.date.strftime('%Y')
        else:
            self.year_of_kpi = False

    @api.onchange('employee_id')
    def _onchange_get_department_kpi(self):
        kpi_master_data = self.env["kpi.master"].search([
            ('department_id', '=', self.employee_id.department_id.id)
        ])

        employee_kpi_list = []
        if kpi_master_data:
            for rec in kpi_master_data.kpi_ids:
                employee_kpi_list += [{
                    'name': rec.name,
                    'rating': '0'
                }]

        self.employee_kpi_ids = [(5, 0, 0)] + [(0, 0, rec) for rec in employee_kpi_list]

    def action_send_kpi_mail(self):
        template_id = self.env.ref('employee_work_performance.email_template_send_kpi')
        if template_id:
            email_values = {
                'email_from': 'hr@africab.com',
                'email_to': self.employee_id.work_email,
                'email_cc': self.employee_id.parent_id.work_email
            }
            template_id.send_mail(self.id, email_values=email_values, force_send=True)

    def action_send_task_mail(self):
        template_id = self.env.ref('employee_work_performance.email_template_send_task')
        if template_id:
            email_values = {
                'email_from': 'hr@africab.com',
                'email_to': self.employee_id.work_email,
                'email_cc': self.employee_id.parent_id.work_email
            }
            template_id.send_mail(self.id, email_values=email_values, force_send=True)

    def action_send_behaviour_mail(self):
        template_id = self.env.ref('employee_work_performance.email_template_send_behaviour')
        if template_id:
            email_values = {
                'email_from': 'hr@africab.com',
                'email_to': self.employee_id.work_email,
                'email_cc': self.employee_id.parent_id.work_email
            }
            template_id.send_mail(self.id, email_values=email_values, force_send=True)

    def action_send_innovation_mail(self):
        template_id = self.env.ref('employee_work_performance.email_template_send_innovation')
        if template_id:
            email_values = {
                'email_from': 'hr@africab.com',
                'email_to': self.employee_id.work_email,
                'email_cc': self.employee_id.parent_id.work_email
            }
            template_id.send_mail(self.id, email_values=email_values, force_send=True)
