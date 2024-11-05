# -*- coding: utf-8 -*-
{
    'name': "Africab Core",

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
    'depends': ['base', 'hr', 'hrms', 'hide_menu_user', 'hide_page_user',
                'model_access_rights', 'odoo_readonly_user', 'access_restriction_by_ip',
                'auto_logout_idle_user_odoo', 'ms_query'],

    # always loaded
    'data': [
        'security/core_security.xml',
        'security/ir.model.access.csv',
        'views/core_menu.xml',
        'views/hide_policy_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}

