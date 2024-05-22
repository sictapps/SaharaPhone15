# -*- coding: utf-8 -*-

"""Sale Order"""
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_purchase_order = fields.Boolean(default=True)
