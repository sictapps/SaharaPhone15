# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    repair_id = fields.Char()


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    repair_cost = fields.Float(string='Margin', compute='_compute_cost')
    inv_total = fields.Float(string='Invoice Total', compute='_compute_inv_total')
    total_cost = fields.Float(string='Invoice Total', compute='_compute_total_cost', store=True)
    total_margin = fields.Float(string='Margin', compute='_compute_Margin', store=True)

    @api.depends('invoice_id.amount_total','amount_total')
    def _compute_cost(self):
        for this in self:
            this.repair_cost = this.pricelist_id.currency_id.round(this.invoice_id.amount_total - this.amount_total)

    @api.depends('invoice_id.amount_total')
    def _compute_inv_total(self):
        for this in self:
            this.inv_total = this.pricelist_id.currency_id.round(this.invoice_id.amount_total)


    @api.depends('inv_total')
    def _compute_total_cost(self):
        for this in self:
            this.total_cost += this.pricelist_id.currency_id.round(this.inv_total)

    @api.depends('inv_total')
    def _compute_Margin(self):
        for this in self:
            this.total_margin += this.pricelist_id.currency_id.round(this.repair_cost)

    repair_count = fields.Integer(compute='compute_count')

    def compute_count(self):
        for record in self:
            record.repair_count = self.env['stock.picking'].search_count(
                [('repair_id', '=', self.name)])

    def return_(self):
        self.ensure_one()

        type = self.env['stock.picking.type'].search([('id', '=', 15)])

        vals = {
            'repair_id': self.name,
            'partner_id': self.partner_id.id,
            'picking_type_id': type.id,
            'location_id': type.default_location_src_id.id,
            'location_dest_id': type.default_location_dest_id.id,
            'move_ids_without_package': []
        }

        for operation in self.operations:
            order1_vals = {
                'product_id': operation.product_id.id,
                'name': operation.product_id.name,
                'product_uom': operation.product_uom.id,
                'location_id': vals['location_id'],
                'location_dest_id': vals['location_dest_id'],
            }

            vals['move_ids_without_package'].append((0, None, order1_vals))

        picking = self.env['stock.picking'].create(vals)

        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
        action['res_id'] = picking.id
        action['context'] = {'default_vals': vals}
        action['target'] = 'new'
        picking.action_confirm()

        lot_ids = self.operations.mapped('lot_id')
        for i in picking.move_line_ids_without_package:
            print(i.lot_id.name, 'stock.immediate.transfer')
            i.lot_id = lot_ids[0]  # set first lot_id by default
            if lot_ids:
                lot_id = lot_ids[0]
                lot_ids = lot_ids[1:]
                i.lot_id = lot_id
            i.qty_done = i.product_uom_qty

        if picking.repair_id:
            # picking.button_validate()
            print('----------')
        else:
            print('++++++++++++')

        return action

    def get_repair(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Repair Return',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('repair_id', '=', self.name)],
            'context': "{'create': False}"
        }
