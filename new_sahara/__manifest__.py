# -*- coding: utf-8 -*-
{
    'name': "new_sahara",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'repair', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/repair_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "assets": {
        "point_of_sale.assets": [
            "new_sahara/static/src/js/Screens/ProductScreen/*",
        ],

    }, }
