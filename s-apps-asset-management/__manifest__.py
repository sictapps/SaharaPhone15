# -*- coding: utf-8 -*-
{
    'name': "s-apps-asset-management",



    'description': """
        Long description of module's purpose
    """,

    'author': "Mouhammad ali",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'asset',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_asset','stock','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
