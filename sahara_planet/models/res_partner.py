# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError

import requests
import json


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    passport_barcode = fields.Char(string='Passport Barcode')
    code = fields.Char(string='Code', tracking=True)
    firstName = fields.Char(string='First Name', tracking=True, readonly=True)
    lastName = fields.Char(string='Last Name', tracking=True, readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", tracking=True)
    phoneNumber = fields.Char(string='Phone Number', tracking=True)
    passportNumber = fields.Char(string='Passport Number', tracking=True, readonly=True)
    expirationDate = fields.Date(string='Expiration Date', tracking=True)
    birthDate = fields.Date(string='Birth Date', tracking=True, readonly=True)
    # country_nationality_id = fields.Many2one(
    #     'res.country', 'Nationality', tracking=True)
    country_nationality_id = fields.Char(
        'Nationality', tracking=True, readonly=True)
    # country_residence_id = fields.Many2one(
    #     'res.country', 'Country Of Residence', tracking=True)
    country_residence_id = fields.Char(
        'Country Of Residence', tracking=True, readonly=True)
    country_birth_id = fields.Many2one(
        'res.country', 'Place Of Birth', tracking=True)
    # issuedBy = fields.Many2one(
    #     'res.country', 'Issued By', tracking=True)
    issuedBy = fields.Char(
        'Issued By', tracking=True, readonly=True)

    # def Passport_Connection(self):
    #     company_field = self.env['res.company'].search([], limit=1)
    #     client_id = company_field.client_id
    #     secret = company_field.client_secret
    #     url = 'https://auth.qa-tax.planetpayment.ae/auth/realms/planet/protocol/openid-connect/token'
    #     payload = {'client_id': '%s' % client_id, 'client_secret': '%s' % secret, 'grant_type': 'client_credentials'}
    #
    #     try:
    #         request = requests.post(url, data=payload)
    #
    #         token = request.json()
    #         return token
    #     except:
    #         response_data = json.loads(request.text)
    #         error_message = response_data.get("message", "Unknown error")
    #         raise AccessError(_(error_message))
    #
    # def passport_information(self):
    #     # verification = self.env['res.company'].search([], limit=1)
    #     token = self.Passport_Connection()
    #     print('token', token)
    #     Authorization = 'Bearer %s' % token['access_token']
    #     print('Authorization', Authorization)
    #     url = 'https://frontoffice.tax.planetpayment.ae/services/transactions/api/v2/mrz-decoded'
    #     self.passport_barcode = self.passport_barcode.replace('\\r\\n', '\r\n')
    #     payload = {"mrz": self.passport_barcode}
    #     print('payload', payload)
    #     try:
    #         requset = requests.post(url, json=payload, headers={'Authorization': '%s' % Authorization})
    #         print('requset', requset.text)
    #         firstName = json.loads(requset.text)['firstName']
    #         lastName = json.loads(requset.text)['lastName']
    #         nationality = json.loads(requset.text)['nationality']
    #         countryOfResidence = json.loads(requset.text)['countryOfResidence']
    #         number = json.loads(requset.text)['shopperIdentityDocument']['number']
    #         issuedBy = json.loads(requset.text)['shopperIdentityDocument']['issuedBy']
    #         birth = json.loads(requset.text)['birth']['date']
    #         print(nationality)
    #         if requset.ok:
    #             # Create a new record in the sent.invoices table
    #
    #             self.sudo().firstName = firstName
    #             self.sudo().lastName = lastName
    #             self.sudo().country_nationality_id = nationality
    #             self.sudo().passportNumber = number
    #             self.sudo().country_residence_id = countryOfResidence
    #             self.sudo().issuedBy = issuedBy
    #             self.sudo().birthDate = birth
    #
    #         else:
    #
    #             response_data = json.loads(requset.text)
    #             error_message = response_data.get("message", "Unknown error")
    #             raise AccessError(_(error_message))
    #     except:
    #         response_data = json.loads(requset.text)
    #         error_message = response_data.get("message", "Unknown error")
    #         raise AccessError(_(error_message))
