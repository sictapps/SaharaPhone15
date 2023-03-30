# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"
#
#     cost_qq = fields.Float('Cost', compute='_compute_cost', store=True)
#
#     def _compute_cost(self):
#         for product in self:
#             if product.team_id.name != 'Sales':
#                 product.costq = product.price_total
#             else:
#                 product.costq = product.price_total - product.margin


class SaleReport(models.Model):
    _inherit = "sale.report"

    costq = fields.Float('Cost', readonly=True)
    margin = fields.Float('Margin')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['costq'] = ",(l.price_total - l.margin) as costq"
        fields['margin'] = ", SUM(l.margin / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS margin"
        groupby += ', (l.price_total - l.margin)'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
