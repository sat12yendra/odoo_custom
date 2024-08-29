# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateKpi(models.Model):
    _name = 'employee.task'
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
        ('5', '5')], 'Rating',
        copy=False, required=True)