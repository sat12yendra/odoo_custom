import ssl
import xmlrpc.client
from odoo import models, fields, api, _
from odoo.exceptions import UserError


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



    def action_test_rpc_connection(self):
        """Test XML-RPC connection using the provided credentials."""
        url = self.rpc_url
        db = self.rpc_db
        username = self.rpc_username
        password = self.rpc_password

        try:
            # Ensure URL ends with /xmlrpc/2/common for authentication
            if not url.endswith('/xmlrpc/2/common'):
                url = f'{url.rstrip("/")}/xmlrpc/2/common'

            # For SSL, create an unverified context (for testing only; not for production use)
            context = ssl._create_unverified_context()

            # Initialize XML-RPC connection with the SSL context
            common = xmlrpc.client.ServerProxy(url, context=context)

            # Authenticate and get the user ID
            uid = common.authenticate(db, username, password, {})

            if uid:
                # Success notification
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _("Connection Test"),
                        'message': _("Connection successful!"),
                        'type': 'success',
                        'sticky': False,
                    },
                }
            else:
                raise UserError(_("Connection failed! Please check the credentials."))

        except xmlrpc.client.ProtocolError as protocol_error:
            raise UserError(_("Protocol error! Please check the URL. Error: %s") % str(protocol_error))
        except xmlrpc.client.Fault as fault_error:
            raise UserError(_("XML-RPC Fault! Error: %s") % str(fault_error))
        except ssl.SSLError as ssl_error:
            raise UserError(_("SSL Error! Please check SSL configuration. Error: %s") % str(ssl_error))
        except Exception as e:
            raise UserError(_("Connection failed! Error: %s") % str(e))

