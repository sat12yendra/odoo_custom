# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeWorkPerformance(models.Model):
    _name = 'employee.work.performance'
    _rec_name = "employee_id"
    _inherit = ['mail.thread']
    _description = 'Create Employee Work Performance'

    @api.depends('employee_kpi_ids', 'employee_kpi_ids.manager_rating', 'employee_kpi_ids.hod_rating',
                 'employee_kpi_ids.management_rating')
    def _compute_kpi_totals(self):
        total_kpi_out_of = 0
        for record in self:
            # Number of reviewers
            reviewer_count = len(record.employee_kpi_ids)

            # Total out of (10 points per reviewer)
            record.kpi_out_of = reviewer_count * 10
            total_kpi_out_of += record.kpi_out_of

            # Initialize rating counts
            total_manager_rating = 0
            total_hod_rating = 0
            total_management_rating = 0

            # Sum up ratings from each reviewer
            for kpi in record.employee_kpi_ids:
                total_manager_rating += int(kpi.manager_rating) if kpi.manager_rating else 0
                total_hod_rating += int(kpi.hod_rating) if kpi.hod_rating else 0
                total_management_rating += int(kpi.management_rating) if kpi.management_rating else 0

            # Set individual rating counts
            record.kpi_manager_rating_count = total_manager_rating
            record.kpi_hod_rating_count = total_hod_rating
            record.kpi_management_rating_count = total_management_rating

            # Total rating count (sum of manager, HOD, and management ratings)
            record.total_kpi_rating_count = total_manager_rating + total_hod_rating + total_management_rating
        self.total_kpi_out_of = total_kpi_out_of * 3

    @api.depends('employee_task_ids', 'employee_task_ids.manager_rating',
                 'employee_task_ids.hod_rating', 'employee_task_ids.management_rating')
    def _compute_task_totals(self):
        total_task_out_of = 0
        for record in self:
            # Number of reviewers
            reviewer_count = len(record.employee_task_ids)

            # Total out of (10 points per reviewer)
            record.task_out_of = reviewer_count * 10
            total_task_out_of += record.task_out_of

            # Initialize rating counts
            total_manager_rating = 0
            total_hod_rating = 0
            total_management_rating = 0

            # Sum up ratings from each reviewer
            for task in record.employee_task_ids:
                total_manager_rating += int(task.manager_rating) if task.manager_rating else 0
                total_hod_rating += int(task.hod_rating) if task.hod_rating else 0
                total_management_rating += int(task.management_rating) if task.management_rating else 0

            # Set individual rating counts
            record.task_manager_rating_count = total_manager_rating
            record.task_hod_rating_count = total_hod_rating
            record.task_management_rating_count = total_management_rating

            # Total rating count (sum of manager, HOD, and management ratings)
            record.total_task_rating_count = total_manager_rating + total_hod_rating + total_management_rating

        self.total_task_out_of = total_task_out_of * 3  # Adjust multiplier as necessary

    @api.depends('employee_behaviour_ids', 'employee_behaviour_ids.manager_rating',
                 'employee_behaviour_ids.hod_rating', 'employee_behaviour_ids.management_rating')
    def _compute_behaviour_totals(self):
        total_behaviour_out_of = 0
        for record in self:
            # Number of reviewers
            reviewer_count = len(record.employee_behaviour_ids)

            # Total out of (10 points per reviewer)
            record.behaviour_out_of = reviewer_count * 10
            total_behaviour_out_of += record.behaviour_out_of

            # Initialize rating counts
            total_manager_rating = 0
            total_hod_rating = 0
            total_management_rating = 0

            # Sum up ratings from each reviewer
            for behaviour in record.employee_behaviour_ids:
                total_manager_rating += int(behaviour.manager_rating) if behaviour.manager_rating else 0
                total_hod_rating += int(behaviour.hod_rating) if behaviour.hod_rating else 0
                total_management_rating += int(behaviour.management_rating) if behaviour.management_rating else 0

            # Set individual rating counts
            record.behaviour_manager_rating_count = total_manager_rating
            record.behaviour_hod_rating_count = total_hod_rating
            record.behaviour_management_rating_count = total_management_rating

            # Total rating count (sum of manager, HOD, and management ratings)
            record.total_behaviour_rating_count = total_manager_rating + total_hod_rating + total_management_rating

        self.total_behaviour_out_of = total_behaviour_out_of * 3

    @api.depends('kpi_reviewer_ids', 'task_reviewer_ids', 'behaviour_reviewer_ids')
    def _compute_reviewer_visibility(self):
        for record in self:
            user = self.env.user
            # Super admin users can see all tabs
            if user.has_group('base.group_system'):
                record.kpi_tab_visible = True
                record.task_tab_visible = True
                record.behaviour_tab_visible = True
            else:
                record.kpi_tab_visible = user.employee_id in record.kpi_reviewer_ids
                record.task_tab_visible = user.employee_id in record.task_reviewer_ids
                record.behaviour_tab_visible = user.employee_id in record.behaviour_reviewer_ids

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
    kpi_note = fields.Text("KPI Note")
    task_note = fields.Text("Task Note")
    behaviour_note = fields.Text("Behaviour Note")
    innovation_note = fields.Text("Innovation Note")

    kpi_manager_rating_count = fields.Integer(string="Manager Rating Count", compute="_compute_kpi_totals")
    kpi_hod_rating_count = fields.Integer(string="Hod Rating Count", compute="_compute_kpi_totals")
    kpi_management_rating_count = fields.Integer(string="Management Rating Count", compute="_compute_kpi_totals")
    kpi_out_of = fields.Integer(string="KPI Out of", compute="_compute_kpi_totals")
    total_kpi_out_of = fields.Integer(string="Total Out of", compute="_compute_kpi_totals")
    total_kpi_rating_count = fields.Integer(string="Total Rating Count", compute="_compute_kpi_totals")

    task_manager_rating_count = fields.Integer(string="Manager Rating Count", compute="_compute_task_totals")
    task_hod_rating_count = fields.Integer(string="Hod Rating Count", compute="_compute_task_totals")
    task_management_rating_count = fields.Integer(string="Management Rating Count", compute="_compute_task_totals")
    task_out_of = fields.Integer(string="Task Out of", compute="_compute_task_totals")
    total_task_out_of = fields.Integer(string="Total Out of", compute="_compute_task_totals")
    total_task_rating_count = fields.Integer(string="Total Rating Count", compute="_compute_task_totals")

    behaviour_manager_rating_count = fields.Integer(string="Manager Rating Count", compute="_compute_behaviour_totals")
    behaviour_hod_rating_count = fields.Integer(string="Hod Rating Count", compute="_compute_behaviour_totals")
    behaviour_management_rating_count = fields.Integer(string="Management Rating Count",
                                                       compute="_compute_behaviour_totals")
    behaviour_out_of = fields.Integer(string="Behaviour Out of", compute="_compute_behaviour_totals")
    total_behaviour_out_of = fields.Integer(string="Total Out of", compute="_compute_behaviour_totals")
    total_behaviour_rating_count = fields.Integer(string="Total Rating Count", compute="_compute_behaviour_totals")

    # Fields to store tab visibility status
    kpi_tab_visible = fields.Boolean(compute="_compute_reviewer_visibility")
    task_tab_visible = fields.Boolean(compute="_compute_reviewer_visibility")
    behaviour_tab_visible = fields.Boolean(compute="_compute_reviewer_visibility")

    kpi_reviewer_ids = fields.Many2many('hr.employee', 'kpi_reviewer_rel',
                                    'reviewer_id', 'kpi_id', string="KPI Reviewer")
    task_reviewer_ids = fields.Many2many('hr.employee', 'task_reviewer_rel',
                                        'reviewer_id', 'task_id', string="Task Reviewer")
    behaviour_reviewer_ids = fields.Many2many('hr.employee', 'behaviour_reviewer_rel',
                                        'reviewer_id', 'behaviour_id', string="Behaviour Reviewer")

    employee_kpi_ids = fields.One2many('employee.kpi',
                                     'employee_work_performance_id', string="Employee KPI")
    employee_task_ids = fields.One2many('employee.task','employee_work_performance_id',
                                        auto_join=True, tring="Employee behaviour")
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
        kpi_reviewer_ids = task_reviewer_ids = behaviour_reviewer_ids = []
        if self.employee_id and self.employee_id.department_id:
            department = self.employee_id.department_id
            kpi_reviewer_ids = department.kpi_reviewer_ids.ids if department.kpi_reviewer_ids else []
            task_reviewer_ids = department.task_reviewer_ids.ids if department.task_reviewer_ids else []
            behaviour_reviewer_ids = department.behaviour_reviewer_ids.ids if department.behaviour_reviewer_ids else []
        self.update({'kpi_reviewer_ids': [(6, 0, kpi_reviewer_ids)],
                     'task_reviewer_ids': [(6, 0, task_reviewer_ids)],
                     'behaviour_reviewer_ids': [(6, 0, behaviour_reviewer_ids)]})
        kpi_master_data = self.env["kpi.master"].search([
            ('department_id', '=', self.employee_id.department_id.id)
        ])

        employee_kpi_list = []
        if kpi_master_data:
            for rec in kpi_master_data.kpi_ids:
                employee_kpi_list += [{
                    'name': rec.name,
                    'manager_rating': '1',
                    'hod_rating': '1',
                    'management_rating': '1',
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

    def action_send_task_mail(self, selected_ids=None):
        template_id = self.env.ref('employee_work_performance.email_template_send_task')
        task_ids = self.env["employee.task"].browse(selected_ids)
        if task_ids:
            task_ids.sudo().update({'state': 'assigned'})
        email_values = {
            'email_from': self.employee_id.parent_id.work_email if self.employee_id.parent_id else '',
            'email_to': self.employee_id.work_email,
            'email_cc': self.employee_id.parent_id.work_email if self.employee_id.parent_id else ''
        }
        if template_id:
            template_id.with_context(task_ids=task_ids).send_mail(self.id, email_values=email_values, force_send=True)

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
