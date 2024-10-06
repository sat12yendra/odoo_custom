# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateTask(models.Model):
    _name = 'employee.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Create Task'

    employee_work_performance_id = fields.Many2one('employee.work.performance',
                                                   string="Employee Work Performance")
    name = fields.Char(string="Task")
    task_create_date = fields.Date(string="Task Create Date")
    task_assign_date = fields.Date(string="Task Assign Date")
    task_completed_date = fields.Date(string="Task Completed Date")
    remarks = fields.Char(string="Remarks")
    rating = fields.Selection([
        ('0', '0'),
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
    ], 'Rating',
        copy=False)
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

    def hello(self):
        print("Hello************************")


class CreateSubTaskLines(models.Model):
    _name = 'employee.subtask.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Create Task'

    employee_sub_task_id = fields.Many2one('employee.task', string="Employee SubTask")
    name = fields.Char(string="Sub Task")
    task_create_date = fields.Date(string="Sub Task Create Date")
    task_assign_date = fields.Date(string="Sub Task Assign Date")
    task_completed_date = fields.Date(string="Sub Task Completed Date")
    remarks = fields.Char(string="Remarks")
    rating = fields.Selection([
        ('0', '0'),
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
    ], 'Rating',
        copy=False)
