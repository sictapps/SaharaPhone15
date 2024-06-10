# -*- coding: utf-8 -*-
"""Purchase Order"""
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_sale_order = fields.Boolean(default=True)
