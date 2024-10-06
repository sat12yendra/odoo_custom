# -*- coding: utf-8 -*-
{
    'name': "Employee Work Performance",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hrms', 'africab_core', 'one2many_mass_select_delete'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'views/behaviour_master_view.xml',
        'views/kpi_master_view.xml',
        'views/employee_work_performance_view.xml',
        'views/employee_task_view.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

