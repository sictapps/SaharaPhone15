from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_line_ids_grouped = fields.One2many('account.move.line', compute='_group_invoice_lines')
    material_total = fields.Float(compute='_group_invoice_lines')
    material_quantity = fields.Float()

    def action_post(self):
        super(AccountMove, self.with_context(repair=True) if self.repair_ids else self).action_post()

    def _group_invoice_lines(self):
        for rec in self:
            rec.material_total = sum(rec.invoice_line_ids.filtered(lambda l: l.product_id.type != 'service')
                                     .mapped("price_total"))
            rec.material_quantity = 1;
            rec.invoice_line_ids_grouped = rec.invoice_line_ids.filtered(lambda l: l.product_id.type == 'service')
