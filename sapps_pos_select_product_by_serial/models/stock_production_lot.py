from odoo import models, fields, api


class StockProductionLotInherited(models.Model):
    _inherit = 'stock.production.lot'

    sale_line_stock_product_lot_id = fields.Many2one('sale.order.line')

    def check_if_lot_exists(self, lots):
        res = self.env['stock.production.lot'].search([('name', 'in', lots)])

        if res and all(item.product_id.available_in_pos for item in res):
            return [{"quantity": item.product_qty, "product_id": item.product_id.id, "name": item.product_id.name, "lot": item.name} for item in res]
        else:
            return []


class StockMoveSaharahInherited(models.Model):
    _inherit = 'stock.move'

    def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None, owner_id=None, strict=True):
        self.ensure_one()
        if 'sapps_from_sale_confirm' in self._context and self._context['sapps_from_sale_confirm'] == True \
                and self.sale_line_id and len(self.sale_line_id.sapps_barcode_chosen_lots) > 0:
            taken_qty = 0
            for lotid in  self.sale_line_id.sapps_barcode_chosen_lots:
                taken_qty = taken_qty + super(StockMoveSaharahInherited, self)._update_reserved_quantity(1, available_quantity, location_id, lot_id=lotid, package_id=package_id, owner_id=owner_id, strict=strict)
            self.sale_line_id.sapps_barcode_chosen_lots = False
            return taken_qty
        else:
            return super(StockMoveSaharahInherited, self)._update_reserved_quantity(need, available_quantity, location_id, lot_id, package_id, owner_id, strict)
