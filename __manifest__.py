# -*- coding: utf-8 -*-

{
    'name': 'Fields log dynamic',
    'version': '1.0.1',
    'author':'Soft-integration',
    'category': 'Tools',
    'summary': 'Fields log dynamic',
    'description': "",
    'depends': [
        'mail'
    ],
    'data': [
        'security/fields_log_dynamic_security.xml',
        'security/ir.model.access.csv',
        'views/ir_model_fields_log_views.xml',
        'views/fields_log_dynamic_action.xml',
        'views/fields_log_dynamic_menuitem.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
