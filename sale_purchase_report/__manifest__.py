# -*- coding: utf-8 -*-

{
    'name': "Sale & Purchase Report",
    'summary': """Mixed Reports of Sale and Purchase order""",
    'description': """Mixed Reports of Sale and Purchase order""",
    'category': 'Sale',
    'version': '15.0.1.0.0',
    'author': 'Mohammad Haitham Salman From SAPPS LLC',
    'website': 'https://www.s-apps.io/',
    'company': 'ٍSapps LLC',
    'maintainer': 'ٍSapps LLC',
    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'reports/sale_purchase_report_views.xml',
        'reports/sale_purchase_pdf_template.xml',
        'wizards/wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/sale_purchase_report/static/src/js/action_manager.js',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
