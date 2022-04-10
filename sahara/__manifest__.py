# -*- coding: utf-8 -*-
{
    'name': "sahara",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Montagab",
    'website': "http://site.s-apps.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'point_of_sale','account_check_printing', 'l10n_us'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/posviews.xml',
        'views/custom_internal_layout.xml',
        'views/custom_receipt_layout.xml',
        'views/pos_templates.xml',
        'views/paymentreceipt.xml',
        'views/receiptview.xml',
        'report/print_check.xml',
        'report/print_check_top.xml',
        'report/print_check_middle.xml',
        'report/print_check_bottom.xml',
        # 'views/sahara_custom_check.xml',
        'views/payment_view.xml'
        #  'views/personviews.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
   'qweb': ['static/src/xml/pos_payment_button_view.xml'],
    'assets':{
             'sahara.assets':[
                    '/sahara/static/src/js/pos_set_price_default.js'
                    '/sahara/views/pos_templates.xml',
                 ],
              'web.report_assets_common': [
                    '/sahara/static/**/*',
                ]
            },
}
