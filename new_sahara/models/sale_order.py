# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    cost_sale = fields.Float('Cost', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['cost_sale'] = ",(l.price_total - l.margin) as cost_sale"
        groupby += ', (l.price_total - l.margin)'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

