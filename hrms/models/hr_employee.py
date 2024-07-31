# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Hr Employee Inherit'

    age = fields.Integer("Age")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')])
    nssf_no = fields.Char("NSSF No.")
    tin_no = fields.Char("Tin No.")
    whatsapp_no = fields.Char("WhatsApp No.")
    pan_no = fields.Binary(string="PAN Card No.")
    pan_no_file_name = fields.Char()
    aadhaar_no = fields.Binary(string="Aadhaar Card No.")
    aadhaar_no_file_name = fields.Char()
    alien_card = fields.Char(string="Alien Card")
    swift_code = fields.Char(string="Swift Code")

    bank_details_line_ids = fields.One2many('res.partner.bank', 'employee_id',
                                            string="Bank Details Lines")


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    branch_name = fields.Char("Branch Name")
    ifsc_code = fields.Char(related='bank_id.bic')
