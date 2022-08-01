# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ReportPaymentDistribution(models.AbstractModel):
    _name = 'report.payment_distribution_by_client.report'

    @api.model
    def _get_report_values(self, docids, data=None):

        report_name = 'payment_distribution_by_client.report'
        res = {'invoice': 'out_invoice', 'bills': 'in_invoice', 'credit_note': 'in_refund', 'debit_note': 'out_refund'}


        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'data' : data,

        }
