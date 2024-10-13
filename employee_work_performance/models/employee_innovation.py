# -*- coding: utf-8 -*-

from odoo import models, fields, api

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


class CreateKpi(models.Model):
    _name = 'employee.innovation'
    _description = 'Employee Create Innovation'

    employee_work_performance_id = fields.Many2one('employee.work.performance',
                                                   string="Employee Work Performance")
    name = fields.Char(string="Innovation")
    manager_rating = fields.Selection(rating, 'Manager Rating', copy=False)
    hod_rating = fields.Selection(rating, 'HOD Rating', copy=False)
    management_rating = fields.Selection(rating, 'Management Rating',
                                         copy=False)
    remarks = fields.Char(string="Remarks")