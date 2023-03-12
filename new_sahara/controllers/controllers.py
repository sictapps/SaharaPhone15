# -*- coding: utf-8 -*-
# from odoo import http


# class NewSahara(http.Controller):
#     @http.route('/new_sahara/new_sahara', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new_sahara/new_sahara/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('new_sahara.listing', {
#             'root': '/new_sahara/new_sahara',
#             'objects': http.request.env['new_sahara.new_sahara'].search([]),
#         })

#     @http.route('/new_sahara/new_sahara/objects/<model("new_sahara.new_sahara"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new_sahara.object', {
#             'object': obj
#         })
