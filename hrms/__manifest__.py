# -*- coding: utf-8 -*-
{
    'name': "hrms",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

