# -*- coding: utf-8 -*-
{
    'name': "Thermal Sale Report",
    'version': '15.0.1.0.0',
    'summary': 'This app allows us to print thermal Sale.',
    'description': 'This app allows us to print thermal Sale.',
    'category': 'Extra Tools',
    'author': "Mohammad Salman in S-apps",
    'website': "https://www.s-apps.io/",
    'company': 'SAPPS LLC',
    'depends': ['base', 'sale'],
    'data': [
        'data/report_paperformat_data.xml',
        'report/thermal_report.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
