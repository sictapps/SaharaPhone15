from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'

    def action_confirm(self):
        if 'returned_moves_with_lots' in self._context and self._context['returned_moves_with_lots'] == True \
        and len(self.move_ids_without_package.sapps_chosen_lot_ids) > 0:
            self._check_company()
            self.mapped('package_level_ids').filtered(lambda pl: pl.state == 'draft' and not pl.move_ids)._generate_moves()
            # call `_action_confirm` on every draft move
            self.mapped('move_lines')\
                .filtered(lambda move: move.state == 'draft')\
                ._action_confirm(merge=False)

            # run scheduler for moves forecasted to not have enough in stock
            self.mapped('move_lines').filtered(lambda move: move.state not in ('draft', 'cancel', 'done'))._trigger_scheduler()
            return True
        else:
            return super(StockPickingInherited, self).action_confirm()


class PurchaseMultipleReturn(models.Model):
    _inherit = 'purchase.order'

    def show_multiple_return_wizard(self):
        self.ensure_one()
        picking_type = self.sudo().env['stock.picking.type'].search([('name', '=', 'Purchase Return')])
        pickings = []
        for p in self.picking_ids:
            if any(m.origin_returned_move_id for m in p.move_ids_without_package):
                continue
            else:
                pickings.append(p.id)
        ids = [[6, False, pickings]]
        res = self.env['stock.return.picking.multiple'].create({
            'picking_ids': ids,
            'original_location_id': self.picking_ids[0].location_id.id,
            'purchase_order_id': self.id,
            'picking_type_id': picking_type.id
        })
        return {
            'name': _('Reverse Purchase Transfers'),
            'view_mode': 'form',
            'res_model': 'stock.return.picking.multiple',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': res.id,
            'context': self.env.context,
        }
