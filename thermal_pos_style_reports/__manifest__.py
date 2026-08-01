# -*- coding: utf-8 -*-
{
    'name': "Thermal Reports (POS Style)",
    'version': '15.0.1.0.0',
    'summary': 'Additional "Thermal (POS Style)" print option for Customer Invoices and Repair Orders.',
    'description': """
Thermal Reports (POS Style)
============================
Fully independent, additive-only module. It does NOT modify, inherit from,
or replace anything in thermal_sale_report or thermal_repair_report - those
two modules keep working exactly as they do today, completely untouched.

This module adds ONE more entry to the Print menu of Customer Invoices
(account.move) and Repair Orders (repair.order): "Thermal (POS Style)".
Its own ir.actions.report records, own QWeb templates, own paperformat -
no shared XML IDs with any existing report.

The visual design mirrors the customized POS receipt in this project
(point_of_sale core OrderReceipt.xml + the custom_pos_receipt module's
xpath additions: "Tax Invoice" title, Client/Tel/Tax ID block, SalesPerson
line, "Additional Details" warranty text): bold monospace font, plain-text
dashed-line separators, right-floated amounts, no boxes/colors/grid
borders, order/invoice reference and date printed at the very bottom.
    """,
    'category': 'Extra Tools',
    'author': "Mohammad Salman in S-apps",
    'website': "https://www.s-apps.io/",
    'company': 'SAPPS LLC',
    # 'sahara' is required for account.move.get_line_lots() (serial/lot
    # lookup, reused rather than reimplemented - same helper already used
    # by thermal_sale_report and the official "Sahara Invoices" report).
    'depends': ['base', 'account', 'repair', 'sahara'],
    # 'qrcode' pip package - same library already used by
    # sahara_planet/models/qr_code.py in this codebase for real QR
    # generation, reused here rather than a second implementation.
    'external_dependencies': {
        'python': ['qrcode'],
    },
    'data': [
        'data/report_paperformat_data.xml',
        'report/thermal_invoice_pos_style_report.xml',
        'report/thermal_repair_pos_style_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
