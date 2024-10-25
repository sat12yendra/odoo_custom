import logging
import base64
import ssl
import xmlrpc.client
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EmployeeRPC(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee XML-RPC Connector'

    def _get_rpc_credentials(self):
        """Retrieve XML-RPC credentials from system settings."""
        config = self.env['ir.config_parameter'].sudo()
        url = config.get_param('rpc_connector.rpc_url')
        db = config.get_param('rpc_connector.rpc_db')
        username = config.get_param('rpc_connector.rpc_username')
        password = config.get_param('rpc_connector.rpc_password')

        if not (url and db and username and password):
            raise UserError("Please configure XML-RPC credentials in settings.")

        return url, db, username, password

    def create_employee(self, employee_data):
        url, db, username, password = self._get_rpc_credentials()

        try:
            # Establish the connection
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(db, username, password, {})

            if uid is None:
                raise UserError("Authentication failed!")

            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

            # Create employee record dynamically with all matched fields
            employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [employee_data])

            return employee_id
        except Exception as e:
            raise UserError(f"Error in XML-RPC call: {str(e)}")

    def button_get_employee_data(self):
        """Fetch employee data based on the selected record's ID and create in target DB."""
        self.ensure_one()  # Ensure we're working with a singleton
        employee_id = self.id
        url, db, username, password = self._get_rpc_credentials()

        try:
            # Fetch employee data from the current Odoo database
            current_employee_data = self.browse(employee_id)
            if not current_employee_data.exists():
                raise UserError(f"No employee data found for ID {employee_id}")

            # Prepare employee_data to pass to create_employee
            employee_data = self.prepare_employee_values(current_employee_data, db, username, password)
            print("sssssssssssssss", employee_data)
            # Call create_employee method to create employee in the target DB
            created_employee_id = self.create_employee(employee_data)

            _logger.info(f"Employee created in target DB with ID: {created_employee_id}")

            return created_employee_id  # Return the created employee ID

        except Exception as e:
            _logger.error(f"Error fetching and creating employee data: {str(e)}")
            raise UserError(f"Error fetching and creating employee data: {str(e)}")

    def prepare_employee_values(self, employee_data, db, uid, password):
        """Prepare employee values based on field types for XML-RPC."""
        employee_values = {}

        # Retrieve employee fields metadata dynamically
        employee_fields = self._get_employee_fields()  # Assuming this method returns a dict with field names as keys and field info as values
        for field_name, field_info in employee_fields.items():
            field_type = field_info.get('type')
            relation = field_info.get('relation')

            if field_name in employee_data:
                field_value = employee_data[field_name]

                # Handle simple field types
                if field_type in ['char', 'text', 'integer', 'float', 'boolean', 'selection']:
                    employee_values[
                        field_name] = field_value if field_value is not None else False  # Replace None with False or omit the field

                # Handle Many2one fields
                # elif field_type == 'many2one':
                #     employee_values[field_name] = field_value if isinstance(field_value, int) else self._get_related_id(
                #         field_value, relation, db, uid, password)

                # Handle Many2many fields
                # elif field_type == 'many2many':
                #     employee_values[field_name] = [(6, 0, field_value)] if isinstance(field_value,
                #                                                                       list) else self._get_related_ids(
                #         field_value, relation, db, uid, password)

                # Handle One2many fields
                # elif field_type == 'one2many':
                #     employee_values[field_name] = self._prepare_sub_records(field_value, relation, db, uid, password)

                # Handle Binary/Image fields
                elif field_type in ['binary', 'image']:
                    if field_value is not None:
                        if isinstance(field_value, bytes):
                            employee_values[field_name] = base64.b64encode(field_value).decode('utf-8')
                        else:
                            employee_values[field_name] = False  # Handle unexpected types
                    else:
                        employee_values[field_name] = False  # No image provided

        return employee_values

    def _get_related_id(self, field_value, relation, db, uid, password):
        """Retrieve related ID for Many2one fields."""
        models = xmlrpc.client.ServerProxy(f'{self._get_rpc_credentials()[0]}/xmlrpc/2/object')
        related_id = models.execute_kw(db, uid, password, relation, 'search', [[['name', '=', field_value]]])
        return related_id[0] if related_id else False

    def _get_related_ids(self, field_value, relation, db, uid, password):
        """Retrieve related IDs for Many2many fields."""
        models = xmlrpc.client.ServerProxy(f'{self._get_rpc_credentials()[0]}/xmlrpc/2/object')
        related_ids = models.execute_kw(db, uid, password, relation, 'search', [[['name', 'in', field_value]]])
        return [(6, 0, related_ids)] if related_ids else []

    def _prepare_sub_records(self, field_value, relation, db, uid, password):
        """Prepare sub-records for One2many fields."""
        sub_records = []
        models = xmlrpc.client.ServerProxy(f'{self._get_rpc_credentials()[0]}/xmlrpc/2/object')

        for sub_data in field_value:
            sub_record_data = {}
            sub_fields = models.execute_kw(db, uid, password, relation, 'fields_get', [],
                                           {'attributes': ['type', 'relation']})

            for sub_field_name, sub_field_info in sub_fields.items():
                if sub_field_name in sub_data:
                    sub_field_type = sub_field_info['type']
                    sub_record_data[sub_field_name] = self._get_sub_field_value(sub_data, sub_field_name,
                                                                                sub_field_type, db, uid, password)

            sub_records.append((0, 0, sub_record_data))  # Prepare sub-record for creation
        return sub_records

    def _get_sub_field_value(self, sub_data, sub_field_name, sub_field_type, db, uid, password):
        """Get the value for a sub-field based on its type."""
        models = xmlrpc.client.ServerProxy(f'{self._get_rpc_credentials()[0]}/xmlrpc/2/object')

        if sub_field_type in ['char', 'integer', 'float', 'boolean', 'selection']:
            return sub_data.get(sub_field_name, False)
        elif sub_field_type == 'many2one':
            related_id = models.execute_kw(db, uid, password, sub_field_info['relation'], 'search',
                                           [[['name', '=', sub_data[sub_field_name]]]])
            return related_id[0] if related_id else False
        elif sub_field_type in ['binary', 'image']:
            return sub_data.get(sub_field_name, False)  # Return binary data directly

        return False

    def _get_employee_fields(self):
        """Retrieve employee fields dynamically, excluding reserved fields."""
        reserved_fields = self._get_reserved_fields()  # Get reserved fields to exclude
        employee_fields = {}

        for field_name in self._fields:
            if field_name not in reserved_fields:
                field_info = self._fields[field_name]
                field_type = field_info.type

                # Check for image fields and handle them appropriately
                if field_type in ['binary', 'image']:
                    employee_fields[field_name] = {
                        'type': field_type,
                        'relation': None  # Image fields don't have a relation
                    }
                else:
                    relation = field_info.relation if hasattr(field_info, 'relation') else None
                    employee_fields[field_name] = {
                        'type': field_type,
                        'relation': relation,
                    }

        return employee_fields

    def _get_reserved_fields(self):
        """Return a list of reserved fields to be excluded."""
        return [
            'id',
            'create_uid',
            'write_uid',
            'create_date',
            'write_date',
            'message_follower_ids',  # Followers on the record
            'message_ids',  # Message records
            'message_main_attachment_id',  # Main attachment for chatter
            'message_posted_before',  # Flag for posted messages
            'message_needaction',  # Indicates if there are unread messages
            'message_has_error',  # Error flag for messages
            'message_count'  # Count of messages
        ]
