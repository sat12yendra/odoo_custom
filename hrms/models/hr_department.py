# -*- coding: utf-8 -*-

from odoo import models, fields

class HrDepartmentInherit(models.Model):
    _inherit = 'hr.department'

    reviewer_ids = fields.Many2many('hr.employee', 'department_reviewer_rel',
                                    'reviewer_id', 'department_id', string="Reviewer")