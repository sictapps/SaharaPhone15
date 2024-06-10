# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sapps_sahara_privacy_policy(models.Model):
#     _name = 'sapps_sahara_privacy_policy.sapps_sahara_privacy_policy'
#     _description = 'sapps_sahara_privacy_policy.sapps_sahara_privacy_policy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
