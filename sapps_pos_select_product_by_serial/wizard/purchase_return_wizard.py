# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round


class BulkReturnPickingLine(models.TransientModel):
    _name = "multiple.transfer.return.picking.line"
    _rec_name = 'product_id'
    _description = 'Return Multiple Transfer'

    product_id = fields.Many2one('product.product', string="Product", required=True, domain="[('id', '=', product_id)]")
    quantity = fields.Float("Quantity", digits='Product Unit of Measure', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    wizard_id = fields.Many2one('stock.return.picking.multiple', string="Wizard")
    move_id = fields.Many2one('stock.move', "Move")
    lot_id = fields.Many2one('stock.production.lot')


class ReturnPicking(models.TransientModel):
    _name = 'stock.return.picking.multiple'
    _inherit = ['barcodes.barcode_events_mixin']
    _description = 'Return Pickings'

    picking_ids = fields.Many2many('stock.picking')
    product_return_moves = fields.One2many('multiple.transfer.return.picking.line', 'wizard_id', 'Moves')
    move_dest_exists = fields.Boolean('Chained Move Exists', readonly=True)
    original_location_id = fields.Many2one('stock.location')
    parent_location_id = fields.Many2one('stock.location')
    company_id = fields.Many2one(related='picking_ids.company_id')
    purchase_order_id = fields.Many2one('purchase.order')
    picking_type_id = fields.Many2one('stock.picking.type')
    location_id = fields.Many2one(
        'stock.location', 'Return Location',
        domain="['|', ('id', '=', original_location_id), '|', '&', ('return_location', '=', True), ('company_id', '=', False), '&', ('return_location', '=', True), ('company_id', '=', company_id)]")

    def on_barcode_scanned(self, barcode):
        if not self.purchase_order_id:
            raise UserError(_("Please choose purchase order to return"))
        move_line = self.picking_ids.move_ids_without_package.mapped('move_line_ids').filtered(lambda v: v.lot_id.name == barcode)
        move = move_line.move_id
        serial = move_line.lot_id
        if move and serial and serial.product_id and serial.product_qty:
            if move.picking_id.state != 'done':
                raise UserError(_("You may only return Done pickings"))

            if len(self.product_return_moves.filtered(lambda v: v.lot_id.id == serial.id)) > 0:
                raise UserError(_("Serial already exists in return order"))
            move_dest_exists = False
            product_return_moves = []
            line_fields = [f for f in self.env['multiple.transfer.return.picking.line']._fields.keys()]
            product_return_moves_data_tmpl = self.env['multiple.transfer.return.picking.line'].default_get(line_fields)
            if move.state == 'cancel':
                raise UserError(_('Move is Canceled'))
            if move.scrapped:
                raise UserError(_('Move is Scrapped'))
            if move.move_dest_ids:
                move_dest_exists = True
            product_return_moves_data = dict(product_return_moves_data_tmpl)
            product_return_moves_data.update(self._prepare_stock_return_picking_line_vals_from_move(move, serial))
            product_return_moves.append(product_return_moves_data)
            if move.picking_id and not product_return_moves:
                raise UserError(
                    _("No products to return (only lines in Done state and not fully returned yet can be returned)."))
            if move.picking_id:
                for val in product_return_moves:
                    obj = self.env['multiple.transfer.return.picking.line'].new(val)
                    self.product_return_moves += obj
                self.move_dest_exists = move_dest_exists
                self.parent_location_id = move.picking_id.picking_type_id.warehouse_id and move.picking_id.picking_type_id.warehouse_id.view_location_id.id or move.picking_id.location_id.location_id.id
                self.original_location_id = move.picking_id.location_id.id
                location_id = move.picking_id.location_id.id
                if move.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
                    location_id = move.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.id
                self.location_id = location_id
        else:
            raise UserError(_("scanned serial is not found in the specified purchase order or it is out of stock. %s"%barcode))

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move(self, stock_move, serial):
        quantity = 1

        quantity = float_round(quantity, precision_rounding=stock_move.product_id.uom_id.rounding)
        return {
            'product_id': stock_move.product_id.id,
            'quantity': quantity,
            'move_id': stock_move.id,
            'uom_id': stock_move.product_id.uom_id.id,
            'lot_id': serial.id,
        }

    def _prepare_move_default_values(self, return_line, new_picking):
        vals = {
            'product_id': return_line.product_id.id,
            'product_uom_qty': return_line.quantity,
            'product_uom': return_line.product_id.uom_id.id,
            'picking_id': new_picking.id,
            'state': 'draft',
            'date': fields.Datetime.now(),
            'location_id': return_line.move_id.location_dest_id.id,
            'location_dest_id': return_line.move_id.location_id.id,
            'picking_type_id': self.picking_type_id.id,
            'warehouse_id': self.picking_type_id.warehouse_id.id,
            'origin_returned_move_id': return_line.move_id.id,
            'procure_method': 'make_to_stock',
            'to_refund': True
        }
        return vals

    def _prepare_picking_default_values(self, picking):
        return {
            'move_lines': [],
            'picking_type_id': picking.picking_type_id.return_picking_type_id.id or picking.picking_type_id.id,
            'state': 'draft',
            'origin': _("Return of %s") % self.purchase_order_id.name,
            'location_id': picking.location_dest_id.id,
            'location_dest_id': self.location_id.id
        }

    def _create_returns(self):
        pickings = self.picking_ids
        # TODO sle: the unreserve of the next moves could be less brutal
        for return_move in self.product_return_moves.mapped('move_id'):
            return_move.move_dest_ids.filtered(lambda m: m.state not in ('done', 'cancel'))._do_unreserve()

        # create new picking for returned products
        # check if all picking have same location, location_dest
        tmp_location_id = pickings[0].location_id
        tmp_location_dest_id = pickings[0].location_dest_id
        if not all(p.location_id.id == tmp_location_id.id and p.location_dest_id.id == tmp_location_dest_id.id for p in pickings):
            raise UserError(_("Please be sure that all pickings have same source/destination location"))

        new_picking = pickings[0].copy(self._prepare_picking_default_values(pickings[0]))
        picking_type_id = new_picking.picking_type_id.id
        # new_picking.message_post_with_view('mail.message_origin_link',
        #     values={'self': new_picking, 'origin': self.picking_id},
        #     subtype_id=self.env.ref('mail.mt_note').id)
        returned_lines = 0
        for return_line in self.product_return_moves:
            if not return_line.move_id:
                raise UserError(_("You have manually created product lines, please delete them to proceed."))
            # TODO sle: float_is_zero?
            if return_line.quantity:
                returned_lines += 1
                vals = self._prepare_move_default_values(return_line, new_picking)
                r = return_line.move_id.copy(vals)
                vals = {}

                # +--------------------------------------------------------------------------------------------------------+
                # |       picking_pick     <--Move Orig--    picking_pack     --Move Dest-->   picking_ship
                # |              | returned_move_ids              ↑                                  | returned_move_ids
                # |              ↓                                | return_line.move_id              ↓
                # |       return pick(Add as dest)          return toLink                    return ship(Add as orig)
                # +--------------------------------------------------------------------------------------------------------+
                move_orig_to_link = return_line.move_id.move_dest_ids.mapped('returned_move_ids')
                # link to original move
                move_orig_to_link |= return_line.move_id
                # link to siblings of original move, if any
                move_orig_to_link |= return_line.move_id\
                    .mapped('move_dest_ids').filtered(lambda m: m.state not in ('cancel'))\
                    .mapped('move_orig_ids').filtered(lambda m: m.state not in ('cancel'))
                move_dest_to_link = return_line.move_id.move_orig_ids.mapped('returned_move_ids')
                # link to children of originally returned moves, if any. Note that the use of
                # 'return_line.move_id.move_orig_ids.returned_move_ids.move_orig_ids.move_dest_ids'
                # instead of 'return_line.move_id.move_orig_ids.move_dest_ids' prevents linking a
                # return directly to the destination moves of its parents. However, the return of
                # the return will be linked to the destination moves.
                move_dest_to_link |= return_line.move_id.move_orig_ids.mapped('returned_move_ids')\
                    .mapped('move_orig_ids').filtered(lambda m: m.state not in ('cancel'))\
                    .mapped('move_dest_ids').filtered(lambda m: m.state not in ('cancel'))
                vals['move_orig_ids'] = [(4, m.id) for m in move_orig_to_link]
                vals['move_dest_ids'] = [(4, m.id) for m in move_dest_to_link]
                r.sapps_chosen_lot_ids = [(4, return_line.lot_id.id)]
                r.write(vals)
        if not returned_lines:
            raise UserError(_("Please specify at least one non-zero quantity."))

        new_picking.with_context(returned_moves_with_lots=True).action_confirm()
        new_picking.with_context(returned_moves_with_lots=True).action_assign()
        return new_picking.id, picking_type_id

    def create_returns(self):
        for wizard in self:
            new_picking_id, pick_type_id = wizard._create_returns()
        # Override the context to disable all the potential filters that could have been set previously
        ctx = dict(self.env.context)
        ctx.update({
            'default_partner_id': self.purchase_order_id.partner_id.id,
            'search_default_picking_type_id': pick_type_id,
            'search_default_draft': False,
            'search_default_assigned': False,
            'search_default_confirmed': False,
            'search_default_ready': False,
            'search_default_planning_issues': False,
            'search_default_available': False,
        })
        return {
            'name': _('Returned Picking'),
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'res_id': new_picking_id,
            'type': 'ir.actions.act_window',
            'context': ctx,
        }
