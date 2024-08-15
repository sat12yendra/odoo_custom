{
    'name': 'Hide Pages for Users',
    'version': '1.0',
    'summary': 'Hide pages based on user access',
    'description': 'This module hides pages in views based on user access rights defined in page categories.',
    'category': 'Hidden',
    'author': 'Your Name',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/page_restriction_views.xml',
    ],
    'installable': True,
    'application': False,
    'assets': {
        'web.assets_backend': [
            'hide_page_user/static/src/js/page_restriction.js',  # Ensure path is correct
        ],
    },
}
