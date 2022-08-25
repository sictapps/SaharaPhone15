from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # def _get_product_accounts(self):
    #     res = super(ProductTemplate, self)._get_product_accounts()
    #     if self._context.get('repair'):
    #         res['income'] = self.property_account_income_id or self.categ_id.property_account_repair_income_categ_id
    #         res['expense'] = self.property_account_expense_id or self.categ_id.property_account_repair_expense_categ_id
    #     return res