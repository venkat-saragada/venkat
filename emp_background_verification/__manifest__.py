# -*- coding: utf-8 -*-
{
    'name': "Employee Background Verification",

    'summary': """
        Employee Background Verification""",

    'description': """
        Employee Background Verification Process
    """,

    'author': "Compassites Software Solutions",
    'website': "http://www.compassitesinc.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','auth_signup'],
    # images
    'images':[
        'static/description/icon.png',
    ],
    # always loaded
    'data': [
        'security/bgv_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        # 'views/referral_category_view.xml',
        'views/referral_checklist_view.xml',
        'views/verification.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}