# -*- coding: utf-8 -*-
# from odoo import http


# class SaharaCommerce(http.Controller):
#     @http.route('/sahara_commerce/sahara_commerce', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sahara_commerce/sahara_commerce/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sahara_commerce.listing', {
#             'root': '/sahara_commerce/sahara_commerce',
#             'objects': http.request.env['sahara_commerce.sahara_commerce'].search([]),
#         })

#     @http.route('/sahara_commerce/sahara_commerce/objects/<model("sahara_commerce.sahara_commerce"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sahara_commerce.object', {
#             'object': obj
#         })
