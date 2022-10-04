# -*- coding: utf-8 -*-
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
                        self.partner_id = partner.id
                        self.jsondata = ""
                else:
                    data = ee['Photo']
                    partner = self.env['res.partner'].create({'EIDNumber' : ee['EIDNumber'],
                        'is_company' : False,
                        'company_type' : 'person',

                        'OccupationFieldCode' : ee['OccupationFieldCode'],
                        'CityID' : ee['CityID'],
                        'OccupationTypeArabic' : ee['OccupationTypeArabic'],
                        'City' : ee['City'],
                        'Area' : ee['Area'],
                        'AreaArabic' : ee['AreaArabic'],
                        'AreaCode' : ee['AreaCode'],
                        'CityArabic' : ee['CityArabic'],
                        'CompanyName' : ee['CompanyName'],
                        'CompanyNameArabic' : ee['CompanyNameArabic'],
                        'DOB' : ee['DOB'],
                        'Email' : ee['Email'],
                        'Emirate' : ee['Emirate'],
                        'EmirateArabic' : ee['EmirateArabic'],
                        'EmirateCode' : ee['EmirateCode'],
                        'Phone' : ee['Phone'],
                        'name' : ee['NameAr'],
                        'email' : ee['Email'],
                        'phone' : ee['Phone'],
                        'mobile' : ee['Mobile'],
                        'Photo' : data,
                        'image_1920' : data,
                        'PhotoPath' : ee['PhotoPath'],
                        'PassportNumber' : ee['PassportNumber'],
                        'Mobile' : ee['Mobile'],
                        'NameAr' : ee['NameAr'],
                        'Name' : ee['Name'],
                        'Nationality' : ee['Nationality'],
                        'NationalityArabic' : ee['NationalityArabic'],
                        'NationalityID' : ee['NationalityID'],
                        'OccupationArabic' : ee['OccupationArabic'],
                        'Occupation' : ee['Occupation'],
                        'OccupationTypeArabic' : ee['OccupationTypeArabic'],
                        'ResidencyType' : ee['ResidencyType'],
                        'ResidencyIssue' : ee['ResidencyIssue'],
                        'ResidencyExpiry' : ee['ResidencyExpiry'],
                        'ResidencyNumber' : ee['ResidencyNumber'],
                        'Sex' : ee['Sex'],
                        'SponsorName' : ee['SponsorName'],
                        'SponsorNumber' : ee['SponsorNumber'],
                        'SponsorType' : ee['SponsorType'],
                        'Signature' : ee['Signature'],
                        'jsondata' : "",

                    })
                    self.partner_id=partner.id



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
                        self.partner_id = partner.id
                        self.jsondata = ""
                else:
                    data = ee['Photo']
                    partner = self.env['res.partner'].create({'EIDNumber': ee['EIDNumber'],
                                                              'is_company': False,
                                                              'company_type': 'person',

                                                              'OccupationFieldCode': ee['OccupationFieldCode'],
                                                              'CityID': ee['CityID'],
                                                              'OccupationTypeArabic': ee['OccupationTypeArabic'],
                                                              'City': ee['City'],
                                                              'Area': ee['Area'],
                                                              'AreaArabic': ee['AreaArabic'],
                                                              'AreaCode': ee['AreaCode'],
                                                              'CityArabic': ee['CityArabic'],
                                                              'CompanyName': ee['CompanyName'],
                                                              'CompanyNameArabic': ee['CompanyNameArabic'],
                                                              'DOB': ee['DOB'],
                                                              'Email': ee['Email'],
                                                              'Emirate': ee['Emirate'],
                                                              'EmirateArabic': ee['EmirateArabic'],
                                                              'EmirateCode': ee['EmirateCode'],
                                                              'Phone': ee['Phone'],
                                                              'name': ee['NameAr'],
                                                              'email': ee['Email'],
                                                              'phone': ee['Phone'],
                                                              'mobile': ee['Mobile'],
                                                              'Photo': data,
                                                              'image_1920': data,
                                                              'PhotoPath': ee['PhotoPath'],
                                                              'PassportNumber': ee['PassportNumber'],
                                                              'Mobile': ee['Mobile'],
                                                              'NameAr': ee['NameAr'],
                                                              'Name': ee['Name'],
                                                              'Nationality': ee['Nationality'],
                                                              'NationalityArabic': ee['NationalityArabic'],
                                                              'NationalityID': ee['NationalityID'],
                                                              'OccupationArabic': ee['OccupationArabic'],
                                                              'Occupation': ee['Occupation'],
                                                              'OccupationTypeArabic': ee['OccupationTypeArabic'],
                                                              'ResidencyType': ee['ResidencyType'],
                                                              'ResidencyIssue': ee['ResidencyIssue'],
                                                              'ResidencyExpiry': ee['ResidencyExpiry'],
                                                              'ResidencyNumber': ee['ResidencyNumber'],
                                                              'Sex': ee['Sex'],
                                                              'SponsorName': ee['SponsorName'],
                                                              'SponsorNumber': ee['SponsorNumber'],
                                                              'SponsorType': ee['SponsorType'],
                                                              'Signature': ee['Signature'],
                                                              'jsondata': "",

                                                              })
                    self.partner_id = partner.id


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
                        self.partner_id = partner.id
                        self.jsondata = ""
                else:
                    data = ee['Photo']
                    partner = self.env['res.partner'].create({'EIDNumber': ee['EIDNumber'],
                                                              'is_company': False,
                                                              'company_type': 'person',

                                                              'OccupationFieldCode': ee['OccupationFieldCode'],
                                                              'CityID': ee['CityID'],
                                                              'OccupationTypeArabic': ee['OccupationTypeArabic'],
                                                              'City': ee['City'],
                                                              'Area': ee['Area'],
                                                              'AreaArabic': ee['AreaArabic'],
                                                              'AreaCode': ee['AreaCode'],
                                                              'CityArabic': ee['CityArabic'],
                                                              'CompanyName': ee['CompanyName'],
                                                              'CompanyNameArabic': ee['CompanyNameArabic'],
                                                              'DOB': ee['DOB'],
                                                              'Email': ee['Email'],
                                                              'Emirate': ee['Emirate'],
                                                              'EmirateArabic': ee['EmirateArabic'],
                                                              'EmirateCode': ee['EmirateCode'],
                                                              'Phone': ee['Phone'],
                                                              'name': ee['NameAr'],
                                                              'email': ee['Email'],
                                                              'phone': ee['Phone'],
                                                              'mobile': ee['Mobile'],
                                                              'Photo': data,
                                                              'image_1920': data,
                                                              'PhotoPath': ee['PhotoPath'],
                                                              'PassportNumber': ee['PassportNumber'],
                                                              'Mobile': ee['Mobile'],
                                                              'NameAr': ee['NameAr'],
                                                              'Name': ee['Name'],
                                                              'Nationality': ee['Nationality'],
                                                              'NationalityArabic': ee['NationalityArabic'],
                                                              'NationalityID': ee['NationalityID'],
                                                              'OccupationArabic': ee['OccupationArabic'],
                                                              'Occupation': ee['Occupation'],
                                                              'OccupationTypeArabic': ee['OccupationTypeArabic'],
                                                              'ResidencyType': ee['ResidencyType'],
                                                              'ResidencyIssue': ee['ResidencyIssue'],
                                                              'ResidencyExpiry': ee['ResidencyExpiry'],
                                                              'ResidencyNumber': ee['ResidencyNumber'],
                                                              'Sex': ee['Sex'],
                                                              'SponsorName': ee['SponsorName'],
                                                              'SponsorNumber': ee['SponsorNumber'],
                                                              'SponsorType': ee['SponsorType'],
                                                              'Signature': ee['Signature'],
                                                              'jsondata': "",

                                                              })
                    self.partner_id = partner.id


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
                        if not self.is_accrual:
                            self.partner_id = partner.id
                        else:
                            self.actual_vendor= partner.id

                        self.jsondata = ""
                else:
                    data = ee['Photo']
                    partner = self.env['res.partner'].create({'EIDNumber': ee['EIDNumber'],
                                                              'is_company': False,
                                                              'company_type': 'person',

                                                              'OccupationFieldCode': ee['OccupationFieldCode'],
                                                              'CityID': ee['CityID'],
                                                              'OccupationTypeArabic': ee['OccupationTypeArabic'],
                                                              'City': ee['City'],
                                                              'Area': ee['Area'],
                                                              'AreaArabic': ee['AreaArabic'],
                                                              'AreaCode': ee['AreaCode'],
                                                              'CityArabic': ee['CityArabic'],
                                                              'CompanyName': ee['CompanyName'],
                                                              'CompanyNameArabic': ee['CompanyNameArabic'],
                                                              'DOB': ee['DOB'],
                                                              'Email': ee['Email'],
                                                              'Emirate': ee['Emirate'],
                                                              'EmirateArabic': ee['EmirateArabic'],
                                                              'EmirateCode': ee['EmirateCode'],
                                                              'Phone': ee['Phone'],
                                                              'name': ee['NameAr'],
                                                              'email': ee['Email'],
                                                              'phone': ee['Phone'],
                                                              'mobile': ee['Mobile'],
                                                              'Photo': data,
                                                              'image_1920': data,
                                                              'PhotoPath': ee['PhotoPath'],
                                                              'PassportNumber': ee['PassportNumber'],
                                                              'Mobile': ee['Mobile'],
                                                              'NameAr': ee['NameAr'],
                                                              'Name': ee['Name'],
                                                              'Nationality': ee['Nationality'],
                                                              'NationalityArabic': ee['NationalityArabic'],
                                                              'NationalityID': ee['NationalityID'],
                                                              'OccupationArabic': ee['OccupationArabic'],
                                                              'Occupation': ee['Occupation'],
                                                              'OccupationTypeArabic': ee['OccupationTypeArabic'],
                                                              'ResidencyType': ee['ResidencyType'],
                                                              'ResidencyIssue': ee['ResidencyIssue'],
                                                              'ResidencyExpiry': ee['ResidencyExpiry'],
                                                              'ResidencyNumber': ee['ResidencyNumber'],
                                                              'Sex': ee['Sex'],
                                                              'SponsorName': ee['SponsorName'],
                                                              'SponsorNumber': ee['SponsorNumber'],
                                                              'SponsorType': ee['SponsorType'],
                                                              'Signature': ee['Signature'],
                                                              'jsondata': "",

                                                             })
                    if not self.is_accrual:
                        self.partner_id = partner.id
                    else:
                        self.actual_vendor = partner.id
        self.write({'is_accrual': False})


class emirate_hid(models.Model):
    _inherit = "res.partner"
    jsondata = fields.Char("-")



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
                    self.jsondata = ""
                    raise exceptions.UserError(
                        _('The Partner  %(empl_name)s, Is Already Exist.') % {
                            'empl_name': partner.name, })

                    self.partner_id = partner.id

            else:
                self.is_company= False
                self.company_type = 'person'
                self.EIDNumber = ee['EIDNumber']
                self.OccupationFieldCode = ee['OccupationFieldCode']
                self.CityID = ee['CityID']
                self.OccupationTypeArabic = ee['OccupationTypeArabic']
                self.City = ee['City']
                self.Area = ee['Area']
                self.AreaArabic = ee['AreaArabic']
                self.AreaCode = ee['AreaCode']
                self.CityArabic = ee['CityArabic']
                self.CompanyName = ee['CompanyName']
                self.CompanyNameArabic = ee['CompanyNameArabic']
                self.DOB = ee['DOB']
                self.Email =  ee['Email']
                self.Emirate = ee['Emirate']
                self.EmirateArabic = ee['EmirateArabic']
                self.EmirateCode = ee['EmirateCode']
                self.Phone = ee['Phone']
                self.name=ee['NameAr']
                self.email=ee['Email'] if len(ee['Email'])>0 else self.email
                self.phone=ee['Phone'] if len(ee['Phone'])>0 else self.phone
                self.mobile=ee['Mobile'] if len(ee['Mobile'])>0 else self.mobile

                data =ee['Photo']


                self.Photo=data
                self.image_1920=data
                self.PhotoPath = ee['PhotoPath']
                self.PassportNumber = ee['PassportNumber']
                self.Mobile = ee['Mobile']
                self.NameAr = ee['NameAr']
                self.Name = ee['Name']
                self.Nationality = ee['Nationality']
                self.NationalityArabic = ee['NationalityArabic']
                self.NationalityID = ee['NationalityID']
                self.OccupationArabic = ee['OccupationArabic']
                self.Occupation = ee['Occupation']
                self.OccupationTypeArabic = ee['OccupationTypeArabic']
                self.ResidencyType = ee['ResidencyType']
                self.ResidencyIssue = ee['ResidencyIssue']
                self.ResidencyExpiry = ee['ResidencyExpiry']
                self.ResidencyNumber = ee['ResidencyNumber']
                self.Sex = ee['Sex']
                self.SponsorName = ee['SponsorName']
                self.SponsorNumber = ee['SponsorNumber']
                self.SponsorType = ee['SponsorType']
                self.Signature = ee['Signature']
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
