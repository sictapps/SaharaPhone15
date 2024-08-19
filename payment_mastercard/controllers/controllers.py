import json

import requests
import logging


from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
_logger = logging.getLogger(__name__)

class MPGSController(http.Controller):
    @http.route('/payment/mpgs/redirect', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    def mpgs_redirect(self, **post):
        reference = post.get('reference')
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', post.get('reference'))])
        _logger.debug("%d is the reference of payment", post.get('reference'))

        if tx:

            credentials = tx.acquirer_id._get_mpgs_credentials()
            mpgs_url = "https://eu-gateway.mastercard.com/api/rest/version/80/merchant/"+credentials['merchant_id']+"/session"
            desc =""
            now = datetime.now()

            # Calculate the date and time for one day after now
            one_day_later = now + timedelta(days=1)

            # Format the date and time in the desired format
            formatted_date = one_day_later.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4] + "Z"

            for order in tx.sale_order_ids:
                for line in order.order_line:
                    desc += " + " + line.product_id.name
            # إعداد البيانات لإعادة التوجيه
            data = {
                'apiOperation': 'INITIATE_CHECKOUT',

                'order': {
                    'amount': tx.amount,
                    'currency': "AED",
                    "description": desc,
                    'id': tx.reference,
                },

                "customer": {"email": tx.partner_email, "firstName": tx.partner_name, "lastName": tx.partner_name,
                             "phone": tx.partner_phone},
                "checkoutMode": "PAYMENT_LINK",
                "paymentLink": {"expiryDateTime": formatted_date, "numberOfAllowedAttempts": 5},
                'interaction': {
                    'operation': 'PURCHASE',
                    'redirectMerchantUrl':request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/my',
                    "returnUrl": request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/payment/mpgs/feedback',
                    # "timeoutUrl": "https://www.google.com",
                    "cancelUrl" :request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/payment/mpgs/feedback',
                    "merchant": {"name": "SAHARA PHONE LLC", "url": "https://www.sahara-e.com"}
                    # 'returnUrl': request.env['ir.config_parameter'].sudo().get_param(
                    #     'web.base.url') + '/payment/mpgs/feedback'
                }
            }




            # إرسال الطلب إلى MPGS والحصول على عنوان إعادة التوجيه
            response = requests.post(mpgs_url, json=data, auth=("merchant."+credentials['merchant_id'], credentials['api_secret']))

            redirect_url = response.json().get('paymentLink').get('url')
            successIndicator= response.json().get('successIndicator')
            tx.write({'successIndicator': successIndicator})
            _logger.debug("%d is the redirect URL", redirect_url)

            return request.redirect(redirect_url, local=False)



    @http.route('/payment/mpgs/feedback', type='http', auth='public', methods=['GET', 'POST'], website=True)
    def mpgs_feedback(self, **post):
        data = request.params


        tx = request.env['payment.transaction'].sudo().search([('successIndicator', '=', post.get('resultIndicator'))])
        if tx:
                tx._set_done()
                return request.redirect(request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/my')



        else:
            return request.redirect('/shop/payment')


