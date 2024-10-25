
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rpc_url = fields.Char(string='RPC URL')
    rpc_db = fields.Char(string='RPC Database')
    rpc_username = fields.Char(string='RPC Username')
    rpc_password = fields.Char(string='RPC Password')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('rpc_connector.rpc_url', self.rpc_url)
        self.env['ir.config_parameter'].sudo().set_param('rpc_connector.rpc_db', self.rpc_db)
        self.env['ir.config_parameter'].sudo().set_param('rpc_connector.rpc_username', self.rpc_username)
        self.env['ir.config_parameter'].sudo().set_param('rpc_connector.rpc_password', self.rpc_password)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            rpc_url=self.env['ir.config_parameter'].sudo().get_param('rpc_connector.rpc_url'),
            rpc_db=self.env['ir.config_parameter'].sudo().get_param('rpc_connector.rpc_db'),
            rpc_username=self.env['ir.config_parameter'].sudo().get_param('rpc_connector.rpc_username'),
            rpc_password=self.env['ir.config_parameter'].sudo().get_param('rpc_connector.rpc_password'),
        )
        return res
