# -*- coding: utf-8 -*-

from odoo import models, fields

class HrDepartmentInherit(models.Model):
    _inherit = 'hr.department'

    kpi_reviewer_ids = fields.Many2many('hr.employee', 'kpi_department_reviewer_rel',
                                    'reviewer_id', 'kpi_department_id', string="KPI Reviewer")
    task_reviewer_ids = fields.Many2many('hr.employee', 'task_department_reviewer_rel',
                                        'reviewer_id', 'task_department_id', string="Task Reviewer")
    behaviour_reviewer_ids = fields.Many2many('hr.employee', 'behaviour_department_reviewer_rel',
                                        'reviewer_id', 'behaviour_department_id',
                                              string="Behaviour Reviewer")