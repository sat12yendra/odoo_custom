# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KpiMaster(models.Model):
    _name = 'kpi.master'
    _description = 'Employee KPI Master'

    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    department_id = fields.Many2one('hr.department', 'Department', check_company=True, required=True)
    kpi_ids = fields.One2many('kpi.master.line',
                                       'kpi_master_id', string="KPIs")


class CreateBehaviour(models.Model):
    _name = 'kpi.master.line'
    _description = 'Employee KPI Master Line'

    name = fields.Char(string="KPI Name")
    kpi_master_id = fields.Many2one('kpi.master', string="KPI Master ID")