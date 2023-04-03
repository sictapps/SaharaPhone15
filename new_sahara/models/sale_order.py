# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = "sale.report"

    cost_sale = fields.Float('Cost', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['cost_sale'] = ",(l.price_total - l.margin) as cost_sale"
        groupby += ', (l.price_total - l.margin)'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    cost_pos = fields.Float('Cost', readonly=True)

    def _select(self):
        return super(PosOrderReport, self)._select() + \
               ',(SUM(ROUND((l.qty * l.price_unit) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END, cu.decimal_places)) - SUM(l.price_subtotal - l.total_cost / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) AS cost_pos'

    # def _group_by(self):
    #     return super(PosOrderReport, self)._group_by() + ',(price_total - margin)'
