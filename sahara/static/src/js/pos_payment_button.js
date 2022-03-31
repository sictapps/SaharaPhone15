odoo.define('sahara.PaymentScreenButton', function(require) {
    'use strict';
       const { Gui } = require('point_of_sale.Gui');
       const PosComponent = require('point_of_sale.PosComponent');
       const { posbus } = require('point_of_sale.utils');
       const ProductScreen = require('point_of_sale.ProductScreen');
       const { useListener } = require('web.custom_hooks');
       const Registries = require('point_of_sale.Registries');
       const PaymentScreen = require('point_of_sale.PaymentScreen');
        const CustomButtonPaymentScreen = (PaymentScreen) =>
           class extends PaymentScreen {
               constructor() {
                   super(...arguments);
                   if (this.currentOrder.is_to_invoice()) {

                         this.currentOrder.set_to_invoice(true);
                   }else{
                         this.currentOrder.set_to_invoice(true)
                   }
                
                //    this.currentOrder.set_to_invoice(true);
               }
               IsCustomButton() {
                   // click_invoice
                    Gui.showPopup("ErrorPopup", {
                           title: this.env._t('Payment Screen Custom Button Clicked'),
                           body: this.env._t('Welcome to OWL'),
                       });
               }
           };
       Registries.Component.extend(PaymentScreen, CustomButtonPaymentScreen);
       return CustomButtonPaymentScreen;
    });