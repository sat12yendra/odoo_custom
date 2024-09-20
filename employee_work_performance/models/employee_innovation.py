# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateKpi(models.Model):
    _name = 'employee.innovation'
    _description = 'Employee Create Innovation'

    employee_work_performance_id = fields.Many2one('employee.work.performance',
                                                   string="Employee Work Performance")
    name = fields.Char(string="Innovation")
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
        ('10', '10')], 'Rating',
        copy=False, required=True)
    remarks = fields.Char(string="Remarks")