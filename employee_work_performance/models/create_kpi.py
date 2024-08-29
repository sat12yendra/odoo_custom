# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateKpi(models.Model):
    _name = 'create.kpi'
    _description = 'Employee Create KPI'

    employee_work_performance_id = fields.Many2one('employee.work.performance',
                                                   string="Employee Work Performance")
    name = fields.Char(string="KPI")
    rating = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')], 'Rating',
        copy=False, required=True)
    remarks = fields.Char(string="Remarks")