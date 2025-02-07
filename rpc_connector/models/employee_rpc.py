import logging
import ssl
import xmlrpc.client
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

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

    # def button_get_employee_data(self):
    #     """Create multiple employees in the target database based on selected records."""
    #     _logger.info("Executing Sync Employee Data Action...")
    #
    #     if not self:
    #         raise UserError("No employees selected. Please select at least one employee.")
    #
    #     url, db, username, password = self._get_rpc_credentials()
    #
    #     try:
    #         context = ssl._create_unverified_context()
    #         common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=context)
    #         uid = common.authenticate(db, username, password, {})
    #
    #         if uid is None:
    #             raise UserError("Authentication failed!")
    #
    #         models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=context)
    #         created_employees = []
    #
    #         for employee in self:
    #             employee_name = employee.name
    #             employee_data = self.prepare_employee_values(employee, models, url, db, uid, password)
    #
    #             # Create the employee in the target database
    #             created_employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [employee_data])
    #             _logger.info(f"Employee '{employee_name}' created in target DB with ID: {created_employee_id}")
    #             created_employees.append((employee_name, created_employee_id))
    #
    #         # Success message
    #         message = "\n".join([f"Employee '{name}' successfully created with ID {emp_id}" for name, emp_id in created_employees])
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': 'Success',
    #                 'message': message,
    #                 'type': 'success',
    #                 'sticky': False,
    #             }
    #         }
    #
    #     except xmlrpc.client.ProtocolError as protocol_error:
    #         _logger.error(f"Protocol error: {str(protocol_error)}")
    #         raise UserError(f"Protocol error! Please check the URL. Error: {str(protocol_error)}")
    #     except xmlrpc.client.Fault as fault_error:
    #         _logger.error(f"XML-RPC Fault: {str(fault_error)}")
    #         raise UserError(f"XML-RPC Fault! Error: {str(fault_error)}")
    #     except ssl.SSLError as ssl_error:
    #         _logger.error(f"SSL Error: {str(ssl_error)}")
    #         raise UserError(f"SSL Error! Please check SSL configuration. Error: {str(ssl_error)}")
    #     except Exception as e:
    #         _logger.error(f"Error fetching and creating employees: {str(e)}")
    #         raise UserError(f"Error fetching and creating employees: {str(e)}")

    def button_get_employee_data(self):
        print("Executing Sync Employee Data Action...")  # Fetch all employees or filter as needed

        url, db, username, password = self._get_rpc_credentials()

        try:


            # Establish the connection to the target database
            context = ssl._create_unverified_context()
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=context)
            uid = common.authenticate(db, username, password, {})

            if uid is None:
                raise UserError("Authentication failed!")

            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=context)
            for employee in self:
                _logger.error(f"Count for employee update:{employee.name}")
                # Extract values for comparison
                employee_name = employee.name
                department_name = employee.department_id.name
                job_name = employee.job_id.name
                manager_name = employee.parent_id.name
                coach_name = employee.coach_id.name

                # Check if employee with the same name already exists in the target DB
                existing_employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search', [
                    [('name', '=', employee_name)]
                ])
                department_id = models.execute_kw(db, uid, password, 'hr.department', 'search', [
                    [('name', '=', department_name)]])
                job_id = models.execute_kw(db, uid, password, 'hr.job', 'search', [
                    [('name', '=', job_name)]])
                parent_id = models.execute_kw(db, uid, password, 'hr.employee', 'search', [
                    [('name', '=', manager_name)]])
                coach_id = models.execute_kw(db, uid, password, 'hr.employee', 'search', [
                    [('name', '=', coach_name)]])


                # Manually set the employee data
                employee_data = {
                    'department_id': department_id[0] if department_id else False,
                    'job_id': job_id[0] if job_id else False,
                    'parent_id': parent_id[0] if parent_id else False,
                    'coach_id': coach_id[0] if coach_id else False,
                    'job_title': employee.job_title
                }

                if existing_employee_ids:
                    # Update the existing record
                    employee_id_to_update = existing_employee_ids[0]

                    resume_line = models.execute_kw(db, uid, password, 'hr.resume.line', 'search', [
                        [('employee_id', '=', employee_id_to_update)]  # Search condition
                        ])
                    resume_id = None
                    if resume_line:
                        resume_id = resume_line[0]
                    resume_line_id = self.env['hr.resume.line'].sudo().search(
                        [('employee_id', '=', employee.id)], limit=1)
                    date_start = None
                    if resume_line_id:
                        date_start = resume_line_id[0].date_start
                    _logger.info(f"Date start**********{resume_id}- {resume_line_id}-{date_start}")
                    # Update resume details
                    if resume_id:
                        models.execute_kw(db, uid, password, 'hr.resume.line', 'write', [
                            [resume_id], {'date_start': date_start}
                        ])


                    # Update bank details
                    bank_line_ids = self.env['res.partner.bank'].sudo().search(
                        [('employee_id', '=', employee.id)])
                    if bank_line_ids:
                        for bank in bank_line_ids:
                            account_no = bank.acc_number
                            account_holder_name = bank.partner_id.name
                            account_holder_id = models.execute_kw(db, uid, password, 'res.partner', 'search', [
                                [('name', '=', account_holder_name)]])
                            new_account_holder_id = None
                            if not account_holder_id:
                                new_account_holder_id = models.execute_kw(db, uid, password, 'res.partner', 'create',
                                                  [{'name': account_holder_name}])
                            bank_details_id = models.execute_kw(db, uid, password, 'res.partner.bank', 'search', [
                                [('acc_number', '=', account_no)]])
                            if not bank_details_id:
                                models.execute_kw(db, uid, password, 'res.partner.bank', 'create',
                                                  [{'employee_id': employee_id_to_update,
                                                    'acc_number': account_no,
                                                    'partner_id': account_holder_id[0] if account_holder_id else new_account_holder_id}])


                    # Update HR Salary Details
                    component_id = self.env['salary.master'].sudo().search(
                        [('name', '=', "Basic Salary")])
                    salary_details_id = self.env['hr.salary.details'].sudo().search(
                        [('employee_id', '=', employee.id),('component_id','=', component_id.id)], limit=1)
                    currency = 135
                    amount = 0.0
                    if salary_details_id:
                        amount = salary_details_id.amount
                    salary_line = models.execute_kw(db, uid, password, 'hr.salary.details', 'search', [
                        [('employee_id', '=', employee_id_to_update),('component_id', '=', 1)]  # Search condition
                    ])
                    if salary_line:
                        salary_id = salary_line[0]
                        _logger.info(f"Salary Details********** {salary_id}-{amount}")
                        models.execute_kw(db, uid, password, 'hr.salary.details', 'write', [
                            [salary_id], {'amount': amount, 'currency_id': currency}
                        ])

                    # Update Employee records
                    models.execute_kw(db, uid, password, 'hr.employee', 'write', [
                        [employee_id_to_update], employee_data
                    ])

                    _logger.info(f"Employee with ID {employee_id_to_update} updated in target DB.")

        except xmlrpc.client.ProtocolError as protocol_error:
            _logger.error(f"Protocol error: {str(protocol_error)}")
            raise UserError(f"Protocol error! Please check the URL. Error: {str(protocol_error)}")
        except xmlrpc.client.Fault as fault_error:
            _logger.error(f"XML-RPC Fault: {str(fault_error)}")
            raise UserError(f"XML-RPC Fault! Error: {str(fault_error)}")
        except ssl.SSLError as ssl_error:
            _logger.error(f"SSL Error: {str(ssl_error)}")
            raise UserError(f"SSL Error! Please check SSL configuration. Error: {str(ssl_error)}")
        except Exception as e:
            _logger.error(f"Error fetching and updating employee data: {str(e)}")
            raise UserError(f"Error fetching and updating employee data: {str(e)}")

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
                # elif field_type == 'many2one':
                #     if field_value:
                #         search_field = field_info.get('search_field', 'display_name')
                #         related_id = self._get_related_id(field_value, field_info['relation'], search_field, models,
                #                                           db, uid, password)
                #         employee_values[field_name] = related_id if related_id else False
                #     else:
                #         employee_values[field_name] = False

                # Handle date and datetime field types
                elif field_type in ['date', 'datetime']:
                    if field_value:
                        employee_values[field_name] = field_value  # Assign the value directly
                    else:
                        employee_values[field_name] = False  # Set to False if no value

                # Handle one2many field types
                # elif field_type == 'one2many':
                #     if field_value:
                #         # Assuming field_value is a list of dictionary items representing related records
                #         related_records = []
                #         for record in field_value:
                #             related_record_values = self.prepare_related_record_values(record, models, url, db, uid,
                #                                                                        password)
                #             if related_record_values:
                #                 related_records.append((0, 0, related_record_values))  # Create command for one2many
                #         employee_values[field_name] = related_records
                #     else:
                #         employee_values[field_name] = []  # Set to empty list if no value

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
                        'relation': None
                    }
                # elif field_type == 'many2one':
                #     # Retrieve the relation from the Many2one field
                #     relation = field_info.comodel_name
                #     employee_fields[field_name] = {
                #         'type': field_type,
                #         'relation': relation,
                #     }
                # elif field_type == 'many2many':
                #     # Retrieve the relation from the Many2many field
                #     relation = field_info.comodel_name
                #     employee_fields[field_name] = {
                #         'type': field_type,
                #         'relation': relation,
                #     }
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
