from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def action_confirm(self):
        self = self.with_context(sapps_from_sale_confirm = True)
        return super(SaleOrder, self).action_confirm()


    def on_barcode_scanned(self, barcode):
        serial = self.env['stock.production.lot'].search([('name', 'ilike', barcode)])
        if serial and serial.product_id and serial.product_id.sale_ok:
            order_lines = self.order_line.filtered(
                lambda r: r.product_id.id == serial.product_id.id)
            if order_lines:
                order_line = order_lines[0]
                qty = order_line.product_uom_qty
                order_line.product_uom_qty = qty + 1
                order_line.sapps_barcode_chosen_lots = [(4, serial.id)]
            else:
                orderLine = self.order_line.new({
                    'product_id': serial.product_id.id,
                    'product_uom_qty': 1,
                    'price_unit': serial.product_id.lst_price,
                    'sapps_barcode_chosen_lots': [(4, serial.id)]
                })
                self.order_line += orderLine
                orderLine.product_id_change()
        else:
            raise UserError(
                'Scanned Serial %s is not defined; or cannot be sold please verify product configuration' %
                barcode)


class SaharaSaleLine(models.Model):
    _inherit = 'sale.order.line'

    sapps_barcode_chosen_lots = fields.One2many('stock.production.lot', inverse_name='sale_line_stock_product_lot_id')
