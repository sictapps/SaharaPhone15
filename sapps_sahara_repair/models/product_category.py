from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    property_account_repair_income_categ_id = fields.Many2one('account.account', company_dependent=True,
        string="Repair Income Account",
        domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used when validating a repair invoice.")
    property_account_repair_expense_categ_id = fields.Many2one('account.account', company_dependent=True,
        string="Repair Expense Account",
        domain="['&', ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="The expense is accounted for when a vendor bill is validated, except in anglo-saxon accounting with perpetual inventory valuation in which case the expense (Cost of Goods Sold account) is recognized at the customer invoice validation.")
