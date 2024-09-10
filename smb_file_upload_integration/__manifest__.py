{
    'name': 'Samba File Upload Integration',
    'version': '1.0',
    'summary': 'Upload files to Samba share and store URL in ir.attachment',
    'category': 'Tools',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/smb_configuration_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
