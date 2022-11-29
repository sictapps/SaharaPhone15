# -*- coding: utf-8 -*-
{
    'name': "sapps_sahara_repair_reports",

    'summary': """
        Somme reports for Sahara""",

    'description': """
        Somme reports for Sahara
    """,

    'author': "Montagab Sheha",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'repair','stock'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'wizards/confirm_without_parts_view.xml'
        'report/repair_reports.xml',
        'report/repair_templates_repair_order.xml',
        'report/report_stockpicking_operations.xml'
    ],
}
