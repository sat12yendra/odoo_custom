# -*- coding: utf-8 -*-

from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
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
    ('10', '10'),
]


class HrApplicantCustom(models.Model):
    _inherit = 'hr.applicant'

    priority = fields.Selection(AVAILABLE_PRIORITIES, "Evaluation", default='0')

