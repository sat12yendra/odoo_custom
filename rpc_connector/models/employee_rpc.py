import logging
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

    def button_get_employee_data(self):
        """Fetch employee data based on the selected record's ID and create or update in target DB."""
        for employee in self:
            url, db, username, password = self._get_rpc_credentials()
            try:
                # Extract values for comparison
                employee_name = employee.name
                employee_email = employee.work_email

                # Establish the connection to the target database
                common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
                uid = common.authenticate(db, username, password, {})

                if uid is None:
                    raise UserError("Authentication failed!")

                models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

                # Check if employee with the same name and work_email already exists in target DB
                existing_employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search', [
                    [('work_email', '=', employee_email)]
                ])

                # Prepare employee data
                employee_data = self.prepare_employee_values(employee, models, url, db, uid, password)

                if existing_employee_ids:
                    # If employee exists, update the existing record
                    employee_id_to_update = existing_employee_ids[0]
                    models.execute_kw(db, uid, password, 'hr.employee', 'write', [
                        [employee_id_to_update], employee_data
                    ])
                    _logger.info(f"Employee with ID {employee_id_to_update} updated in target DB.")
                    message = f"Employee '{employee_name}' successfully updated in the target database with ID {employee_id_to_update}."
                else:
                    # If employee does not exist, create a new record
                    created_employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [employee_data])
                    _logger.info(f"Employee created in target DB with ID: {created_employee_id}")
                    message = f"Employee '{employee_name}' successfully created in the target database with ID {created_employee_id}."

                # Success message
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success',
                        'message': message,
                        'type': 'success',
                        'sticky': False,
                    }
                }

            except Exception as e:
                _logger.error(f"Error fetching and creating or updating employee data: {str(e)}")
                raise UserError(f"Error fetching and creating or updating employee data: {str(e)}")

    def prepare_employee_values(self, employee_data, models, url, db, uid, password):
        """Prepare employee values based on field types for XML-RPC."""
        employee_values = {}

        # Retrieve employee fields metadata dynamically
        employee_fields = self._get_employee_fields()
        for field_name, field_info in employee_fields.items():
            field_type = field_info.get('type')

            if field_name in employee_data:
                field_value = employee_data[field_name]

                # Handle simple field types
                if field_type in ['char', 'text', 'integer', 'float', 'boolean', 'selection']:
                    employee_values[field_name] = field_value if field_value is not None else False

                # Handle binary and image field types
                elif field_type in ['binary', 'image']:
                    employee_values[field_name] = field_value if field_value else False

                # Handle many2one field types
                elif field_type == 'many2one':
                    if field_value:
                        search_field = field_info.get('search_field', 'display_name')
                        related_id = self._get_related_id(field_value, field_info['relation'], search_field, models,
                                                          db, uid, password)
                        employee_values[field_name] = related_id if related_id else False
                    else:
                        employee_values[field_name] = False

                # Handle date and datetime field types
                elif field_type in ['date', 'datetime']:
                    if field_value:
                        employee_values[field_name] = field_value  # Assign the value directly
                    else:
                        employee_values[field_name] = False  # Set to False if no value

                # Handle one2many field types
                elif field_type == 'one2many':
                    if field_value:
                        # Assuming field_value is a list of dictionary items representing related records
                        related_records = []
                        for record in field_value:
                            related_record_values = self.prepare_related_record_values(record, models, url, db, uid,
                                                                                       password)
                            if related_record_values:
                                related_records.append((0, 0, related_record_values))  # Create command for one2many
                        employee_values[field_name] = related_records
                    else:
                        employee_values[field_name] = []  # Set to empty list if no value

        return employee_values

    def prepare_related_record_values(self, record_data, models, url, db, uid, password):
        """Prepare values for related one2many records."""
        related_values = {}

        # Assuming the same logic as prepare_employee_values to extract values
        related_fields = self._get_employee_fields()  # Retrieve related fields metadata
        for field_name, field_info in related_fields.items():
            field_type = field_info.get('type')

            if field_name in record_data:
                field_value = record_data[field_name]

                # Handle field types similar to the main employee data
                if field_type in ['char', 'text', 'integer', 'float', 'boolean', 'selection']:
                    related_values[field_name] = field_value if field_value is not None else False
                elif field_type in ['binary', 'image']:
                    related_values[field_name] = field_value if field_value else False
                elif field_type in ['date', 'datetime']:
                    related_values[field_name] = field_value if field_value else False
                # Add more field types as necessary...

        return related_values

    def _get_related_id(self, field_value, relation, search_field, models, db, uid, password):
        """Retrieve related ID for Many2one fields."""
        related_id = models.execute_kw(db, uid, password, relation, 'search', [[[search_field, '=', field_value.display_name]]])
        return related_id[0] if related_id else False

    def _get_related_ids(self, field_values, relation, models, db, uid, password):
        """Retrieve related IDs for Many2many fields based on display names."""
        related_ids = []
        if field_values:
            # Search for related IDs based on display names
            for display_name in field_values:
                search_ids = models.execute_kw(db, uid, password, relation, 'search', [[['name', '=', display_name]]])
                related_ids.extend(search_ids)

        return [(6, 0, related_ids)] if related_ids else []

    def _get_employee_fields(self):
        """Retrieve employee fields dynamically, excluding reserved fields."""
        reserved_fields = self._get_reserved_fields()  # Get reserved fields to exclude
        employee_fields = {}

        for field_name, field_info in self._fields.items():
            if field_name not in reserved_fields:
                field_type = field_info.type

                # Check for image fields and handle them appropriately
                if field_type in ['binary', 'image']:
                    employee_fields[field_name] = {
                        'type': field_type,
                        'relation': None  # Image fields don't have a relation
                    }
                elif field_type == 'many2one':
                    # Retrieve the relation from the Many2one field
                    relation = field_info.comodel_name
                    employee_fields[field_name] = {
                        'type': field_type,
                        'relation': relation,
                    }
                elif field_type == 'many2many':
                    # Retrieve the relation from the Many2many field
                    relation = field_info.comodel_name
                    employee_fields[field_name] = {
                        'type': field_type,
                        'relation': relation,
                    }
                else:
                    employee_fields[field_name] = {
                        'type': field_type,
                        'relation': None  # Simple fields
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
