# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _name = 'salary.master'
    _description = 'Hr Employee Salary Master'

    name = fields.Char(string="Component")
    salary_type = fields.Selection([('in_hand', 'In-hand'), ('others', 'Others')],
                                   string="Salary Type")
