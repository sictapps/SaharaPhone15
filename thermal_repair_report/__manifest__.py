# -*- coding: utf-8 -*-
{
    'name': "Thermal Repair Order",
    'version': '15.0.1.0.0',
    'summary': 'Thermal (58mm/80mm) print report for Repair Orders.',
    'description': """
Adds a "Thermal Repair Order" print option to Repair Orders, using the same
visual identity (header/footer/typography/paper formats) as the Thermal
Invoice report from the thermal_sale_report module.

This module is fully isolated: it does not modify repair.order business
logic, does not touch the standard "Print Repair Order" report, and does
not alter any accounting/invoicing behaviour.
    """,
    'category': 'Extra Tools',
    'author': "Mohammad Salman in S-apps",
    'website': "https://www.s-apps.io/",
    'company': 'SAPPS LLC',
    'depends': ['base', 'repair', 'thermal_sale_report'],
    'data': [
        'report/thermal_repair_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
