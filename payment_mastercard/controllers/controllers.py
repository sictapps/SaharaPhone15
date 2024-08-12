import requests
import logging


from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class MPGSController(http.Controller):
    @http.route('/payment/mpgs/redirect', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    def mpgs_redirect(self, **post):
        reference = post.get('reference')
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', post.get('reference'))])
        _logger.debug("%d is the reference of payment", post.get('reference'))
        # self.message_post(body=post.get('reference'))
        if tx:

            credentials = tx.acquirer_id._get_mpgs_credentials()
            mpgs_url = "https://eu-gateway.mastercard.com/api/rest/version/80/merchant/"+credentials['merchant_id']+"/session"
            desc =""
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

                "customer": {"email": "peteMorris@mail.us.com", "firstName": "John", "lastName": "Doe",
                             "mobilePhone": "+971 544210311", "phone": "+971 544210311"},
                "checkoutMode": "PAYMENT_LINK",
                "paymentLink": {"expiryDateTime": "2024-09-25T10:00:00.04Z", "numberOfAllowedAttempts": 5},
                "3DSecure": {
                    "acsReturnUrl": request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/payment/mpgs/feedback',
                },
                'interaction': {
                    'operation': 'PURCHASE',
                    'redirectMerchantUrl':request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/payment/mpgs/feedback',
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
            _logger.debug("%d is the redirect URL", redirect_url)

            return request.redirect(redirect_url, local=False)



    @http.route('/payment/mpgs/feedback', type='http', auth='public', methods=['GET', 'POST'], website=True)
    def mpgs_feedback(self, **post):
        data = request.params
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', data.get('order_id'))])
        if tx:
            if data.get('result') == 'SUCCESS':
                tx.write({'state': 'done'})
            else:
                tx.write({'state': 'error', 'state_message': data.get('error_description', 'Unknown error')})
            return request.render('payment_mpgs.payment_feedback', {'transaction': tx})
        else:
            return request.redirect('/shop/payment')


