# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    def return_(self):
        self.ensure_one()

        type = self.env['stock.picking.type'].search([('id', '=', 1)])

        vals = {
            'partner_id': self.partner_id.id,
            'picking_type_id': type.id,
            'location_id': self.partner_id.property_stock_supplier.id,
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

        return action
