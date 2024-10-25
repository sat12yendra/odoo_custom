{
    'name': 'Employee XML-RPC Connector',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Extra Tools',
    'summary': 'Module to connect and create employees via XML-RPC',
    'description': """
        This module allows for creating employee records via XML-RPC dynamically
        by handling different field types (char, integer, float, Many2one, Many2many, One2many).
    """,
    'depends': ['base', 'hr'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/employee_form_view.xml',
    ],
    'installable': True,
    'application': True,
}
