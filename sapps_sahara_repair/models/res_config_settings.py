# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    location_id = fields.Many2one(
        'stock.location', string='Repair Loss Spare Parts',
        domain="[('usage', '!=', 'internal'), ('usage', '!=', 'view')]",
        config_parameter='repair.default_location')
    repair_area_id = fields.Many2one(
        'stock.location', string='Repair Area',
        domain="[('usage', '!=', 'view')]",
        config_parameter='repair.repair_area')

    picking_type_id = fields.Many2one('stock.picking.type',
                                      string='Raw Material Operation Type', config_parameter='repair.operation_type')

    transfer_product_op = fields.Many2one('stock.picking.type',
                                      string='Receipt Device From Customer', config_parameter='repair.transfer_product_op')

    transfer_product_receipt_new_serial = fields.Many2one('stock.picking.type',
                                             string='',
                                             config_parameter='repair.receipt_new_serial')

    repair_service_product = fields.Many2one('product.product',
                                             string='Repair Service Product',
                                             config_parameter='repair.repair_service_product')
