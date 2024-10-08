# -*- coding: utf-8 -*-
import re

from PIL import Image
import io
from odoo import models, fields, api, http, tools, exceptions, _
import json
import base64


class emirate_hid_repair(models.Model):
    _inherit = "repair.order"
    jsondata = fields.Char("-")

    @api.onchange('jsondata')
    def updateD(self):
        if self.jsondata:
            ee = json.loads(self.jsondata)
            if ee['HasData']:
                self.jsondata = ""

                EIDNumber = ee['EIDNumber']
                partners = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])
                if partners:
                    partner = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])[0]
                    if partner:
                        partner._write({'name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})
                        partner._write({'NameAr': re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['NameAr']))})
                        partner._write({'Name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})
                        self.partner_id = partner.id
                        self.jsondata = ""
                else:
                        self.is_company = False
                        self.company_type = 'person'
                        self.EIDNumber = ee['EIDNumber']
                        self.OccupationTypeArabic = ee['Occupation']
                        self.City = ee['City']
                        self.Area = ee['Area']
                        self.CompanyName = ee['CompanyName']
                        self.DOB = ee['DOB']
                        self.Email = ee['Email']
                        self.Emirate = ee['Emirate']
                        self.Phone = ee['Phone']
                        self.name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))
                        self.email = ee['Email'] if len(ee['Email']) > 0 else self.email
                        self.phone = ee['Phone'] if len(ee['Phone']) > 0 else self.phone
                        self.mobile = ee['Mobile'] if len(ee['Mobile']) > 0 else self.mobile
                        self.PassportNumber = ee['PassportNumber']
                        self.Mobile = ee['Mobile']
                        self.NameAr = re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Occupation = ee['Occupation']
                        self.ResidencyType = ee['ResidencyType']
                        self.ResidencyExpiry = ee['ResidencyExpiry']
                        self.ResidencyNumber = ee['ResidencyNumber']
                        self.Sex = ee['Sex']
                        self.SponsorName = ee['SponsorName']
                        self.SponsorNumber = ee['SponsorNumber']
                        self.SponsorType = ee['SponsorType']
                        self.Nationality = ee['Nationality']
                        self.NationalityArabic = ee['NationalityArabic']
                        image_base64_string = ee.get('Photo')
                        self.image_1920 = image_base64_string
                        self.jsondata = ""



class emirate_hid_sale(models.Model):
    _inherit = "sale.order"
    jsondata = fields.Char("-")

    @api.onchange('jsondata')
    def updateD(self):
        if self.jsondata:
            ee = json.loads(self.jsondata)
            if ee['HasData']:
                self.jsondata = ""

                EIDNumber = ee['EIDNumber']
                partners = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])
                if partners:
                    partner = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])[0]
                    if partner:
                        partner._write({'name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})
                        partner._write({'NameAr': re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['NameAr']))})
                        partner._write({'Name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})

                        self.partner_id = partner.id
                        self.jsondata = ""
                else:
                        self.is_company = False
                        self.company_type = 'person'
                        self.EIDNumber = ee['EIDNumber']
                        self.OccupationTypeArabic = ee['Occupation']
                        self.City = ee['City']
                        self.Area = ee['Area']
                        self.CompanyName = ee['CompanyName']
                        self.DOB = ee['DOB']
                        self.Email = ee['Email']
                        self.Emirate = ee['Emirate']
                        self.Phone = ee['Phone']
                        self.name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))
                        self.email = ee['Email'] if len(ee['Email']) > 0 else self.email
                        self.phone = ee['Phone'] if len(ee['Phone']) > 0 else self.phone
                        self.mobile = ee['Mobile'] if len(ee['Mobile']) > 0 else self.mobile
                        self.PassportNumber = ee['PassportNumber']
                        self.Mobile = ee['Mobile']
                        self.NameAr = re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Occupation = ee['Occupation']
                        self.ResidencyType = ee['ResidencyType']
                        self.ResidencyExpiry = ee['ResidencyExpiry']
                        self.ResidencyNumber = ee['ResidencyNumber']
                        self.Sex = ee['Sex']
                        self.SponsorName = ee['SponsorName']
                        self.SponsorNumber = ee['SponsorNumber']
                        self.SponsorType = ee['SponsorType']
                        self.Nationality = ee['Nationality']
                        self.NationalityArabic = ee['NationalityArabic']
                        image_base64_string = ee.get('Photo')
                        self.image_1920 = image_base64_string
                        self.jsondata = ""


class emirate_hid_purchase(models.Model):
    _inherit = "purchase.order"
    jsondata = fields.Char("-")

    @api.onchange('jsondata')
    def updateD(self):
        if self.jsondata:
            ee = json.loads(self.jsondata)
            if ee['HasData']:
                self.jsondata = ""
                EIDNumber = ee['EIDNumber']
                partners = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])
                if partners:
                    partner = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])[0]
                    if partner:
                        partner._write({'name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})
                        partner._write({'NameAr': re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['NameAr']))})
                        partner._write({'Name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})

                        self.partner_id = partner.id
                        self.jsondata = ""
                else:
                        self.is_company = False
                        self.company_type = 'person'
                        self.EIDNumber = ee['EIDNumber']
                        self.OccupationTypeArabic = ee['Occupation']
                        self.City = ee['City']
                        self.Area = ee['Area']
                        self.CompanyName = ee['CompanyName']
                        self.DOB = ee['DOB']
                        self.Email = ee['Email']
                        self.Emirate = ee['Emirate']
                        self.Phone = ee['Phone']
                        self.name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))
                        self.email = ee['Email'] if len(ee['Email']) > 0 else self.email
                        self.phone = ee['Phone'] if len(ee['Phone']) > 0 else self.phone
                        self.mobile = ee['Mobile'] if len(ee['Mobile']) > 0 else self.mobile
                        self.PassportNumber = ee['PassportNumber']
                        self.Mobile = ee['Mobile']
                        self.NameAr = re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Occupation = ee['Occupation']
                        self.ResidencyType = ee['ResidencyType']
                        self.ResidencyExpiry = ee['ResidencyExpiry']
                        self.ResidencyNumber = ee['ResidencyNumber']
                        self.Sex = ee['Sex']
                        self.SponsorName = ee['SponsorName']
                        self.SponsorNumber = ee['SponsorNumber']
                        self.SponsorType = ee['SponsorType']
                        self.Nationality = ee['Nationality']
                        self.NationalityArabic = ee['NationalityArabic']
                        image_base64_string = ee.get('Photo')
                        self.image_1920 = image_base64_string
                        self.jsondata = ""


class emirate_hid_account(models.Model):
    _inherit = "account.move"
    jsondata = fields.Char("-")

    is_accrual= fields.Boolean(default=False)



    def accrual(self):
        self.write({'is_accrual': True})


    @api.onchange('jsondata')
    def updateD(self):
        if self.jsondata:
            ee = json.loads(self.jsondata)
            if ee['HasData']:
                self.jsondata = ""

                EIDNumber = ee['EIDNumber']
                partners = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])
                if partners:
                    partner = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])[0]
                    if partner:
                        partner._write({'name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})
                        partner._write({'NameAr': re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['NameAr']))})
                        partner._write({'Name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))})
                        partner.name=partner.Name
                        if not self.is_accrual:
                            self.partner_id = partner.id
                        else:
                            self.actual_vendor= partner.id

                        self.jsondata = ""
                else:
                        self.is_company = False
                        self.company_type = 'person'
                        self.EIDNumber = ee['EIDNumber']
                        self.OccupationTypeArabic = ee['Occupation']
                        self.City = ee['City']
                        self.Area = ee['Area']
                        self.CompanyName = ee['CompanyName']
                        self.DOB = ee['DOB']
                        self.Email = ee['Email']
                        self.Emirate = ee['Emirate']
                        self.Phone = ee['Phone']
                        self.name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))
                        self.email = ee['Email'] if len(ee['Email']) > 0 else self.email
                        self.phone = ee['Phone'] if len(ee['Phone']) > 0 else self.phone
                        self.mobile = ee['Mobile'] if len(ee['Mobile']) > 0 else self.mobile
                        self.PassportNumber = ee['PassportNumber']
                        self.Mobile = ee['Mobile']
                        self.NameAr = re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name'])),
                        self.Occupation = ee['Occupation']
                        self.ResidencyType = ee['ResidencyType']
                        self.ResidencyExpiry = ee['ResidencyExpiry']
                        self.ResidencyNumber = ee['ResidencyNumber']
                        self.Sex = ee['Sex']
                        self.SponsorName = ee['SponsorName']
                        self.SponsorNumber = ee['SponsorNumber']
                        self.SponsorType = ee['SponsorType']
                        self.Nationality = ee['Nationality']
                        self.NationalityArabic = ee['NationalityArabic']
                        image_base64_string = ee.get('Photo')
                        self.image_1920 = image_base64_string
                        self.jsondata = ""
        self.write({'is_accrual': False})


class emirate_hid(models.Model):
    _inherit = "res.partner"
    jsondata = fields.Char("-")

    @api.model_create_multi
    def create(self, vals):
        return super(emirate_hid, self).create(vals)


    @api.onchange('jsondata')
    def updateD(self):
        if self.jsondata:
            ee=json.loads(self.jsondata)
            self.jsondata = ""
            EIDNumber = ee['EIDNumber']
            partners = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])
            if partners:
                partner = self.env['res.partner'].search([('EIDNumber', '=', EIDNumber)])[0]
                if partner:
                    partner._write({'name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']) )})
                    partner._write({'NameAr': re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['NameAr']) )})
                    partner._write({'Name': re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']) )})
                    image_base64_string = ee.get('Photo')


                    partner.write({'image_1920':image_base64_string})



                    self.jsondata = ""
                    raise exceptions.UserError(
                        _('The Partner  %(empl_name)s, Is Already Exist.') % {
                            'empl_name': partner.name, })





            else:
                self.is_company= False
                self.company_type = 'person'
                self.EIDNumber = ee['EIDNumber']
                self.OccupationTypeArabic = ee['Occupation']
                self.City = ee['City']
                self.Area = ee['Area']
                self.CompanyName = ee['CompanyName']
                self.DOB = ee['DOB']
                self.Email =  ee['Email']
                self.Emirate = ee['Emirate']
                self.Phone = ee['Phone']
                self.name=re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name']))
                self.email=ee['Email'] if len(ee['Email'])>0 else self.email
                self.phone=ee['Phone'] if len(ee['Phone'])>0 else self.phone
                self.mobile=ee['Mobile'] if len(ee['Mobile'])>0 else self.mobile
                self.PassportNumber = ee['PassportNumber']
                self.Mobile = ee['Mobile']
                self.NameAr = re.sub(r'[^\u0600-\u06FF\s]', '', re.sub(r",+", " ", ee['Name'])),
                self.Name = re.sub(r'[^A-Za-z\s]', '', re.sub(r",+", " ", ee['Name'])),
                self.Occupation = ee['Occupation']
                self.ResidencyType = ee['ResidencyType']
                self.ResidencyExpiry=ee['ResidencyExpiry']
                self.ResidencyNumber = ee['ResidencyNumber']
                self.Sex = ee['Sex']
                self.SponsorName = ee['SponsorName']
                self.SponsorNumber = ee['SponsorNumber']
                self.SponsorType = ee['SponsorType']
                self.Nationality= ee['Nationality']
                self.NationalityArabic = ee['NationalityArabic']
                image_base64_string = ee.get('Photo')
                self.image_1920 = image_base64_string
                self.jsondata=""







    EIDNumber  = fields.Char("EIDNumber")

     
    Name  = fields.Char("Name")

     
    NameAr  = fields.Char("NameAr")

     
    Phone  = fields.Char("Phone")

     
    Mobile  = fields.Char("Mobile")

     
    Email  = fields.Char("Email")

     
    Pobox  = fields.Char("Pobox")

     
    EmirateCode  = fields.Char("EmirateCode")

     
    EmirateArabic  = fields.Char("EmirateArabic")

     
    Emirate  = fields.Char("Emirate")

     
    City  = fields.Char("City")

     
    CityArabic  = fields.Char("CityArabic")

     
    CityID  = fields.Char("CityID")

     
    AreaCode  = fields.Char("AreaCode")

     
    AreaArabic  = fields.Char("AreaArabic")

     
    Area  = fields.Char("Area")

     
    Sex  = fields.Char("Sex")

     
    OccupationCode  = fields.Char("OccupationCode")

     
    OccupationArabic  = fields.Char("OccupationArabic")

     
    Occupation  = fields.Char("Occupation")

     
    OccupationFieldCode  = fields.Char("OccupationFieldCode")

     
    OccupationTypeArabic  = fields.Char("OccupationTypeArabic")

     
    OccupationType  = fields.Char("OccupationType")

     
    SponsorType  = fields.Char("SponsorType")

     
    ResidencyType  = fields.Char("ResidencyType")

     
    DOB  = fields.Char("DOB")

     
    ResidencyIssue  = fields.Char("ResidencyIssue")

     
    ResidencyExpiry  = fields.Char("ResidencyExpiry")

     
    Title  = fields.Char("Title")

     
    TitleAr  = fields.Char("TitleAr")

     
    NationalityID  = fields.Char("NationalityID")

     
    Nationality  = fields.Char("Nationality")

     
    NationalityArabic  = fields.Char("NationalityArabic")

     
    PassportNumber  = fields.Char("PassportNumber")

     
    SponsorNumber  = fields.Char("SponsorNumber")

     
    SponsorName  = fields.Char("SponsorName")

     
    CompanyName  = fields.Char("CompanyName")

     
    CompanyNameArabic  = fields.Char("CompanyNameArabic")

     
    ResidencyNumber  = fields.Char("ResidencyNumber")

     
    cardVersion  = fields.Char("cardVersion")

     
    PhotoPath  = fields.Char("PhotoPath")

     
    Photo  = fields.Image("Photo")

     
    Signature  = fields.Char("Signature")

#     _name = 'emirate_hid.emirate_hid'
#     _description = 'emirate_hid.emirate_hid'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
