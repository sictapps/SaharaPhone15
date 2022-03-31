# -*- coding: utf-8 -*-
# from odoo import http


# class Shyhaa(http.Controller):
#     @http.route('/shyhaa/shyhaa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shyhaa/shyhaa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shyhaa.listing', {
#             'root': '/shyhaa/shyhaa',
#             'objects': http.request.env['shyhaa.shyhaa'].search([]),
#         })

#     @http.route('/shyhaa/shyhaa/objects/<model("shyhaa.shyhaa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shyhaa.object', {
#             'object': obj
#         })
