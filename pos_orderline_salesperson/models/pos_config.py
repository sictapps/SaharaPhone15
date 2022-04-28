# -*- coding: utf-8 -*-

from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    allow_orderline_user = fields.Boolean(string='Allow Orderline Salesperson', help='Allow custom salesperson on Orderlines')
    salespersons = fields.Many2one('hr.employee')

    # def get_all_employees(self):
    #        self.salespersons = self.env['hr.employee'].search([])