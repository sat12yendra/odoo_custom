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
