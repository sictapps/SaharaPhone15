from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError
# from odoo.exceptions import ValidationError, UserError

import requests
import json
import pytz


class AddFullOrder(models.Model):
    _inherit = 'pos.order'
    _description = 'Add Full Order'

    tag_number = fields.Char(string="tagNumber", readonly=True)
    tax_free = fields.Char(string='Tax Notes', readonly=True)

    @api.model
    def _order_fields(self, ui_order):
        res = super(AddFullOrder, self)._order_fields(ui_order)
        res['tax_free'] = ui_order['tax_free_pos'] if ui_order['tax_free_pos'] else False
        return res

    def send_order_pos(self):
        pos_order = self.env['pos.order'].search([], limit=1)
        if pos_order.tax_free == 'Tax free':
            verification = self.env['res.company'].search([], limit=1)
            token = verification.connection_pos()
            url = 'https://frontoffice.qa-tax.planetpayment.ae/services/transactions/api/v2/new-transaction'
            pos_config = self.env['pos.config'].search([], limit=1)
            receiptNumber = pos_order.account_move.name
            date_order = pos_order.date_order.strftime('%Y-%m-%dT%H:%M')
            terminal = pos_config.terminal_code
            total = pos_order.amount_total
            vatIncl = pos_order.amount_tax
            totalBeforeVAT = total - vatIncl
            pm_code = pos_order.account_move.order_payment_method
            pm_name = pos_order.account_move.order_payment_method
            pm_total = pos_order.amount_total
            firstName = pos_order.partner_id.firstName
            lastName = pos_order.partner_id.lastName
            country_nationality_id = pos_order.partner_id.country_nationality_id.code
            country_residence_id = pos_order.partner_id.country_residence_id.code
            phoneNumber = pos_order.partner_id.phoneNumber
            birthDate = pos_order.partner_id.birthDate
            issuedBy = pos_order.partner_id.issuedBy.code
            passportNumber = pos_order.partner_id.passportNumber

            payload = {'issueTaxRefundTag': True, 'date': '%s' % date_order, 'receiptNumber': '%s' % receiptNumber,
                       'terminal': '%s' % terminal, 'taxFreeId': '', 'type': 'RECEIPT',
                       "order": {"totalBeforeVAT": '%s' % totalBeforeVAT, "vatIncl": '%s' % vatIncl,
                                 "total": '%s' % total,
                                 "items": [{"grossAmount": '%s' % i.price_total, "code": '', "departmentCode": '',
                                            "netAmount": '%s' % i.price_unit, "description": '%s' % i.name,
                                            "discountAmount": None, "quantity": '%s' % i.quantity, "serialNumber": '',
                                            "unitPrice": '%s' % i.price_unit, "vatRate": '5', "vatCode": '5',
                                            "vatAmount": '%s' % (i.price_total - i.price_unit),
                                            "merchandiseGroup": '121',
                                            "taxRefundEligible": True} for i in
                                           pos_order.account_move.invoice_line_ids],
                                 "paymentMethods": [{"code": '%s' % pm_code, "name": '%s' % pm_name,
                                                     "amount": '%s' % pm_total}]},
                       "shopper": {"firstName": '%s' % firstName, "lastName": '%s' % lastName,
                                   "nationality": '%s' % country_nationality_id,
                                   "countryOfResidence": '%s' % country_residence_id, "phoneNumber": '%s' % phoneNumber,
                                   "birth": {"date": '%s' % birthDate},
                                   "shopperIdentityDocument": {"type": 'PASSPORT',
                                                               "issuedBy": '%s' % issuedBy,
                                                               "number": '%s' % passportNumber}
                                   }

                       }

            try:
                Authorization = 'Bearer %s' % token['access_token']
                req = requests.post(url, json=payload, headers={'Authorization': '%s' % Authorization})
                tag_number = json.loads(req.text)['taxRefundResponse']['taxRefundTagNumber']

                print('**2', req.text)
                if req.ok:
                    pos_order.sudo().tag_number = tag_number
                    pos_order.sudo().account_move.tag_num = tag_number
                    print('**1', tag_number)

            except:
                raise AccessError(_('%s' % req.text))
            return tag_number

    def get_tag(self):
        pos_order = self.env['pos.order'].search([], limit=1)

        tag_number = pos_order.tag_number
        print(tag_number, '.......................')
        return tag_number

    def _prepare_invoice_vals(self):
        vals = super()._prepare_invoice_vals()

        vals.update({'tag_num': self.tag_number})
        print('***************', vals['tag_num'])
        return vals
