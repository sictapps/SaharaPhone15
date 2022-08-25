# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sapps_netc_repair(models.Model):
#     _name = 'sapps_netc_repair.sapps_netc_repair'
#     _description = 'sapps_netc_repair.sapps_netc_repair'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
