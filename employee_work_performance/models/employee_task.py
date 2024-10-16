# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

rating = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]


class CreateTask(models.Model):
    _name = 'employee.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Create Task'

    def _compute_access_rights(self):
        user = self.env.user
        for record in self:
            record.is_hod = user.has_group('hrms.group_hr_hod')
            record.is_super_admin = user.has_group('base.group_system')

    employee_work_performance_id = fields.Many2one('employee.work.performance',
                                                   string="Employee Work Performance")
    name = fields.Char(string="Task")
    task_create_date = fields.Date(string="Task Create Date")
    task_assign_date = fields.Date(string="Task Assign Date")
    task_tat_date = fields.Date(string="Task TAT Date")
    task_completed_date = fields.Date(string="Task Completed Date")
    manager_remarks = fields.Char(string="Manager Remarks")
    hod_remarks = fields.Char(string="HOD Remarks")
    management_remarks = fields.Char(string="Management Remarks")
    manager_rating = fields.Selection(rating, 'Manager Rating', copy=False)
    hod_rating = fields.Selection(rating, 'HOD Rating', copy=False)
    management_rating = fields.Selection(rating, 'Management Rating',
                                         copy=False)
    is_hod = fields.Boolean(compute='_compute_access_rights')
    is_super_admin = fields.Boolean(compute='_compute_access_rights')
    note = fields.Text("Note")

    state = fields.Selection([
        ('a_new', 'New'),
        ('assigned', 'Assigned'),
        ('b_delayed', 'Delayed'),
        ('completed', 'Completed'),
    ], string='Task Status', default='a_new')
    sub_task_line_ids = fields.One2many('employee.subtask.line',
                                        'employee_sub_task_id', string="Sub Task Lines")

    def action_done(self):
        """
        This is used to make employee task done
        """
        self.state = 'completed'

    @api.model
    def check_tat_date(self):
        today = date.today()
        tasks_to_delay = self.search([('task_tat_date', '<', today), ('state', 'not in', ['a_new', 'b_delayed', 'completed'])])

        for task in tasks_to_delay:
            task.state = 'b_delayed'
            self.send_task_delayed_email(task)

    def send_task_delayed_email(self, task):
        # Assuming the task has a related employee, and employee has a manager
        if (task.user_id and task.employee_work_performance_id.employee_id and \
                task.employee_work_performance_id.employee_id.parent_id):
            manager = task.employee_work_performance_id.employee_id.parent_id
            email_to = manager.work_email  # Manager's email

            if email_to:
                template = self.env.ref('employee_work_performance.task_delayed_email_template')
                template.email_to = email_to
                template.send_mail(task.id, force_send=True)


class CreateSubTaskLines(models.Model):
    _name = 'employee.subtask.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Create Task'

    def _compute_access_rights(self):
        user = self.env.user
        for record in self:
            record.is_hod = user.has_group('hrms.group_hr_hod')
            record.is_super_admin = user.has_group('base.group_system')

    employee_sub_task_id = fields.Many2one('employee.task', string="Employee SubTask")
    name = fields.Char(string="Sub Task")
    task_create_date = fields.Date(string="Sub Task Create Date")
    task_assign_date = fields.Date(string="Sub Task Assign Date")
    task_completed_date = fields.Date(string="Sub Task Completed Date")
    manager_remarks = fields.Char(string="Manager Remarks")
    hod_remarks = fields.Char(string="HOD Remarks")
    management_remarks = fields.Char(string="Management Remarks")
    manager_rating = fields.Selection(rating, 'Manager Rating', copy=False)
    hod_rating = fields.Selection(rating, 'HOD Rating', copy=False)
    management_rating = fields.Selection(rating, 'Management Rating',
                                         copy=False)

    is_hod = fields.Boolean(compute='_compute_access_rights')
    is_super_admin = fields.Boolean(compute='_compute_access_rights')
