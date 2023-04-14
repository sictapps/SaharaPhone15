from odoo import models, api, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_repair_id = fields.Many2one('repair.order')
    product_repair_id = fields.Many2one('repair.order')

    @api.onchange('move_line_ids_without_package')
    def onchange_move_lines_repair(self):
        if 'from_repair' in self._context and self._context['from_repair'] and not self.material_repair_id:
            for rec in self:
                rec.move_lines = [(0, 0, mv) for mv in self._context['default_move_ids_without_package']]
                rec._get_move_ids_without_package()
            self = self.with_context(from_repair=False, default_move_ids_without_package=[])

    def action_assign(self):
        return super(StockPicking, self).action_assign()


class StockMoveNetcRepair(models.Model):
    _inherit = 'stock.move'
    operation_id = fields.Many2one('repair.line')

    def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None, owner_id=None, strict=True):
        self.ensure_one()
        if self.picking_id.product_repair_id:
            taken_qty = super(StockMoveNetcRepair, self)\
                ._update_reserved_quantity(1, available_quantity, location_id, lot_id=self.picking_id.product_repair_id.lot_id,
                                           package_id=package_id, owner_id=owner_id, strict=strict)
            return taken_qty
        elif self.picking_id.material_repair_id:
            taken_qty = 0
            for rec in self.picking_id.material_repair_id.operations.filtered(lambda v: v.product_id.id == self.product_id.id):
                taken_qty += super(StockMoveNetcRepair, self) \
                    ._update_reserved_quantity(1, available_quantity, location_id,
                                               lot_id=rec.lot_id,
                                               package_id=package_id, owner_id=owner_id, strict=strict)
            return taken_qty
        else:
            return super(StockMoveNetcRepair, self)._update_reserved_quantity(need, available_quantity,
                                                                              location_id, lot_id, package_id,
                                                                              owner_id, strict)

    def _should_bypass_reservation(self, forced_location=False):
        if self.picking_id and self.picking_id.product_repair_id and self.picking_id.location_id.usage == 'customer':
            return False
        else:
            return super(StockMoveNetcRepair, self)._should_bypass_reservation(forced_location=forced_location)
