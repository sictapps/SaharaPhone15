# -*- coding: utf-8 -*-
{
    'name': "sapps_sahara_repair",

    'summary': """
        Extends Repair module to support internal, external, repair""",

    'description': """
        Extends Repair module to support internal, external, repair
    """,

    'author': "Ali Ali, Iyad Kentar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'repair', 'stock_account'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config_settings_views.xml',
        'views/product_category.xml',
        'views/stock_picking_views.xml',
        'views/sapps_netc_repair_report.xml',
        'views/sapps_netc_repair_view.xml',
        # 'wizards/confirm_without_parts_view.xml'
    ],
}
