import os
import subprocess
from odoo import models, fields, api
from odoo.exceptions import UserError

class SmbConfiguration(models.Model):
    _name = 'smb.configuration'
    _description = 'Samba Configuration'

    name = fields.Char(string='Configuration Name', required=True)
    smb_ip = fields.Char(string='Samba IP Address', required=True)
    smb_username = fields.Char(string='Samba Username', required=True)
    smb_password = fields.Char(string='Samba Password', required=True)
    smb_share_folder = fields.Char(string='Samba Share Folder', required=True)
    smb_mount_point = fields.Char(string='Mount Point', default='/mnt/samba_share')

    def test_smb_connection(self):
        """
        Test the Samba connection using the provided details.
        """
        self.ensure_one()
        try:
            # Create the smb_mount_point directory if it does not exist
            if not os.path.exists(self.smb_mount_point):
                os.makedirs(self.smb_mount_point, exist_ok=True)

            # Command to test the SMB connection
            smbclient_command = [
                'smbclient',
                f"//{self.smb_ip}/{self.smb_share_folder}",
                '-U', f"{self.smb_username}%{self.smb_password}",
                '-c', 'ls'
            ]

            # Execute the command
            result = subprocess.run(smbclient_command, capture_output=True, text=True)

            # Check for any errors
            if result.returncode != 0:
                raise UserError(f"Failed to connect to SMB share: {result.stderr.strip()}")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Successful',
                    'message': 'Successfully connected to the Samba share.',
                    'type': 'success',
                    'sticky': False,
                }
            }

        except subprocess.CalledProcessError as e:
            raise UserError(f"Error testing Samba connection: {e.output.strip()}")

        except Exception as e:
            raise UserError(f"Error testing Samba connection: {str(e)}")
