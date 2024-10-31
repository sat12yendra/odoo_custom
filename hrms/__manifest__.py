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
    'depends': ['base', 'hr', 'hr_skills', 'resource', 'ps_binary_field_attachment_preview'],

    # always loaded
    'data': [
        'security/hrms_security.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/email_template.xml',
        'data/hr_salary_data.xml',
        'views/hr_employee_views.xml',
        'views/salary_master_view.xml',
        'views/hr_department_view.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-

