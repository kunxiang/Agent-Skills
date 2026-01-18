# -*- coding: utf-8 -*-
{
    'name': 'Full Module Example',
    'version': '18.0.1.0.0',
    'category': 'Services',
    'summary': 'Complete module with all components',
    'description': """
Full Module Example
===================

This module demonstrates a complete Odoo module structure with:
- Models with various field types
- Tree, Form, Kanban, and Search views
- Security groups and access control
- Report definitions
- Demo data

Features:
- Feature 1
- Feature 2
- Feature 3
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        # Security (must be first)
        'security/security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/my_model_views.xml',
        'views/my_model_line_views.xml',
        'views/menus.xml',
        # Data
        'data/sequence_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'full_module/static/src/js/**/*',
            # 'full_module/static/src/css/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
