# -*- coding: utf-8 -*-
from odoo import http


class PrivacyPolicy(http.Controller):
    @http.route('/privacy_policy', auth='public', website=True)
    def index(self):
        return http.request.render('sapps_sahara_privacy_policy.privacy_policy')

    @http.route('/terms_of_service', auth='public', website=True)
    def index1(self):
        return http.request.render('sapps_sahara_privacy_policy.terms_of_service')

    @http.route('/return_policy', auth='public', website=True)
    def index2(self):
        return http.request.render('sapps_sahara_privacy_policy.return_policy')