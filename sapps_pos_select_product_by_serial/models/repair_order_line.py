from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'repair.order'
    _inherit = ['repair.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        serial = self.env['stock.production.lot'].search([('name', '=', barcode)])
        if serial and serial.product_id:
            operation = self.operations.new({
                'product_id': serial.product_id.id,
                'product_uom_qty': 1,
                'price_unit': serial.product_id.standard_price,
                'lot_id': serial.id,
                # 'sapps_barcode_chosen_lots': [(4, serial.id)]
            })
            self.operations += operation
            operation.onchange_product_id()
            operation.sapps_onchange_product_id()
            operation.tax_id = False
        else:
            raise UserError(
                'Scanned Serial %s is not defined; or cannot be sold please verify product configuration' %
                barcode)
