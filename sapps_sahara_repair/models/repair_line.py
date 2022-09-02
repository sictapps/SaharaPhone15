from odoo import models, api


class RepairLine(models.Model):
    _inherit = 'repair.line'

    @api.onchange('product_id')
    def sapps_onchange_product_id(self):
        default_location_id = self.env['ir.config_parameter'].sudo().get_param('repair.repair_area')
        repair_area = self.env["stock.location"].search([('id', '=', default_location_id)], limit=1)
        for rec in self:
            rec.price_unit = self.product_id.standard_price
            rec.location_id = repair_area
            rec.location_dest_id = rec.repair_id.location_id

    @api.onchange('type', 'repair_id')
    def onchange_operation_type(self):
        pass
