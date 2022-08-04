# -*- coding: utf-8 -*-

{
    'name': 'Payment Distribution by client',
    'category': 'accounting',

    'summary': 'Distribute payment into multiple invoices, bills and credit notes',
    'depends': ['account'],
    'data': ['wizard/payment_distribution_view.xml',
             'wizard/payment_distribution_report.xml',
             'report/payment_distribution_templates.xml',
             'security/ir.model.access.csv',
             ],
    'application': False,
    "images":['static/description/banner.png'],
    'license': 'OPL-1',
}
