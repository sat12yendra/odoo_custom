from odoo import models, fields, api


class PageConfiguration(models.Model):
    _name = 'page.configuration'
    _description = 'Page Configuration'

    name = fields.Char(string='Name', required=True)


class ResUsers(models.Model):
    _inherit = 'res.users'

    page_configuration_ids = fields.Many2many(
        'page.configuration',
        string='Page Configurations'
    )

    @api.model
    def get_user_page_configurations(self):
        return self.env.user.page_configuration_ids.mapped('name')