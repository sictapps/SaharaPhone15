from odoo import api, fields, models
import requests
import json


class PaymentMPGS(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('mpgs', 'MPGS')],ondelete={'mpgs': 'set default'})

    mpgs_api_key = fields.Char('MPGS API Key', required_if_provider='mpgs')
    mpgs_api_secret = fields.Char('MPGS API Secret', required_if_provider='mpgs')
    mpgs_merchant_id = fields.Char('MPGS Merchant ID', required_if_provider='mpgs')

    def _get_mpgs_api_url(self, endpoint):
        base_url = "https://api-gateway.mastercard.com"
        return f"{base_url}/{endpoint}"

    def _get_mpgs_credentials(self):
        return {
            'api_key': self.mpgs_api_key,
            'api_secret': self.mpgs_api_secret,
            'merchant_id': self.mpgs_merchant_id
        }

    def mpgs_form_generate_values(self, values):
        values.update({
            'api_key': self._get_mpgs_credentials()['api_key'],
            'api_secret': self._get_mpgs_credentials()['api_secret'],
            'merchant_id': self._get_mpgs_credentials()['merchant_id'],
        })
        return values

    def mpgs_get_form_action_url(self):
        return "/payment/mpgs/feedback"

    def action_initiate_checkout(self, payment_data):
        url = self._get_mpgs_api_url("api/rest/version/80/merchant/{merchant_id}/order")
        credentials = self._get_mpgs_credentials()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + (credentials['api_key'] + ':' + credentials['api_secret']).encode(
                'ascii').strip().decode('ascii')
        }

        response = requests.post(
            url,
            data=json.dumps(payment_data),
            headers=headers
        )

        return response.json()

    def action_mpgs_payment(self, payment_data):
        checkout_response = self.action_initiate_checkout(payment_data)
        if checkout_response.get('result') != 'SUCCESS':
            return checkout_response

        payment_url = self._get_mpgs_api_url("api/rest/version/55/merchant/{merchant_id}/transaction")
        credentials = self._get_mpgs_credentials()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + (credentials['api_key'] + ':' + credentials['api_secret']).encode(
                'ascii').strip().decode('ascii')
        }

        response = requests.post(
            payment_url,
            data=json.dumps(payment_data),
            headers=headers
        )

        return response.json()
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    desc = fields.Char()
    successIndicator = fields.Char()



    def _get_specific_rendering_values(self, processing_values):
        self.ensure_one()
        if self.acquirer_id.provider != 'mpgs':
            return super(PaymentTransaction, self)._get_specific_rendering_values(processing_values)
        desc =""
        for order in self.sale_order_ids:
            for line in order.order_line:
                desc +=" + " +line.product_id.name





        mpgs_values = {
            'reference': self.reference,
            'amount': self.amount,
            'currency': self.currency_id.name,
            'desc':desc


        }
        return mpgs_values
