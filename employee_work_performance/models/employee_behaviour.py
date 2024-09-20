# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateBehaviour(models.Model):
    _name = 'employee.behaviour'
    _description = 'Employee Create Behaviour'

    employee_work_performance_id = fields.Many2one('employee.work.performance',
                                                   string="Employee Work Performance")
    name = fields.Many2one("behaviour.master", string="Behaviour")
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