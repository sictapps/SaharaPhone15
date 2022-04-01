# -*- coding: utf-8 -*-
# from odoo import http


# class EmirateHid(http.Controller):
#     @http.route('/emirate_hid/emirate_hid/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emirate_hid/emirate_hid/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emirate_hid.listing', {
#             'root': '/emirate_hid/emirate_hid',
#             'objects': http.request.env['emirate_hid.emirate_hid'].search([]),
#         })

#     @http.route('/emirate_hid/emirate_hid/objects/<model("emirate_hid.emirate_hid"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emirate_hid.object', {
#             'object': obj
#         })
