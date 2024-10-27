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


class EmployeeInnovation(models.Model):
    _name = 'employee.innovation'
    _description = 'Employee Create Innovation'

    def _compute_access_rights(self):
        user = self.env.user
        for record in self:
            record.is_hod = user.has_group('hrms.group_hr_hod')
            record.is_super_admin = user.has_group('base.group_system')

    employee_work_performance_id = fields.Many2one('employee.work.performance',
                                                   string="Employee Work Performance")
    name = fields.Char(string="Innovation")
    manager_rating = fields.Selection(rating, 'Manager Rating', copy=False)
    hod_rating = fields.Selection(rating, 'HOD Rating', copy=False)
    management_rating = fields.Selection(rating, 'Management Rating',
                                         copy=False)
    manager_remarks = fields.Char(string="Manager Remarks")
    hod_remarks = fields.Char(string="HOD Remarks")
    management_remarks = fields.Char(string="Management Remarks")

    is_hod = fields.Boolean(compute='_compute_access_rights')
    is_super_admin = fields.Boolean(compute='_compute_access_rights')