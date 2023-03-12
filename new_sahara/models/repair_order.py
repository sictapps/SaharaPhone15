# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    repair_id = fields.Char()


class RepairOrder(models.Model):
    _inherit = 'repair.order'

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
