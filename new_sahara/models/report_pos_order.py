# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    cost_pos = fields.Float('Cost', readonly=True)

    def _select(self):
        return super(PosOrderReport, self)._select() + \
               ',(SUM(ROUND((l.qty * l.price_subtotal_incl) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END, cu.decimal_places)) - SUM(l.price_subtotal - l.total_cost / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) AS cost_pos'
