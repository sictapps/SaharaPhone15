# -*- coding: utf-8 -*-
# from odoo import http


# class AssetProduct(http.Controller):
#     @http.route('/s-apps-asset-management/s-apps-asset-management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/s-apps-asset-management/s-apps-asset-management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('s-apps-asset-management.listing', {
#             'root': '/s-apps-asset-management/s-apps-asset-management',
#             'objects': http.request.env['s-apps-asset-management.s-apps-asset-management'].search([]),
#         })

#     @http.route('/s-apps-asset-management/s-apps-asset-management/objects/<model("s-apps-asset-management.s-apps-asset-management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('s-apps-asset-management.object', {
#             'object': obj
#         })
