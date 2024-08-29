# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateBehaviour(models.Model):
    _name = 'create.behaviour'
    _description = 'Employee Create Behaviour Master'

    name = fields.Char(string="Behaviour Name")