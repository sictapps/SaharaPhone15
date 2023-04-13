# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    repair_cost = fields.Float(string='Margin', compute='_compute_cost')
    inv_total = fields.Float(string='Invoice Total', compute='_compute_inv_total')
    total_cost = fields.Float(string='Margin', compute='_compute_computed_repair_cost', store=True)
    total_margin = fields.Float(string='Invoice Total', compute='_compute_computed_inv_total', store=True)

    @api.depends('invoice_id.amount_total', 'amount_total', 'state')
    def _compute_cost(self):
        for order in self:
            if order.state == 'done':
                order.repair_cost = order.invoice_id.amount_total - order.amount_total
            else:
                order.repair_cost = 0.0

    @api.depends('invoice_id.amount_total')
    def _compute_inv_total(self):
        for order in self:
            if order.state == 'done':
                order.inv_total = order.invoice_id.amount_total
            else:
                order.inv_total = 0.0

    @api.depends('repair_cost')
    def _compute_computed_repair_cost(self):
        for order in self:
            order.total_cost = order.repair_cost

    @api.depends('inv_total')
    def _compute_computed_inv_total(self):
        for order in self:
            order.total_margin = order.inv_total
