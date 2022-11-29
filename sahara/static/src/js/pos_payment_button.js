odoo.define('sahara.PaymentScreenButton', function (require) {
    'use strict';
    const {Gui} = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const {posbus} = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const {useListener} = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const CustomButtonPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
                if (this.currentOrder.is_to_invoice()) {

                    this.currentOrder.set_to_invoice(true);
                } else {
                    this.currentOrder.set_to_invoice(true)
                }


                //    this.currentOrder.set_to_invoice(true);
            }

            is_salesperson() {
                for (let id in this.currentOrder.get_orderlines()) {
                    if (!this.currentOrder.get_orderlines()[id].salesperson) {
                        return false
                    } else
                        return true
                }
            }

            async _isOrderValid(isForceValidate) {

                if (this.currentOrder.get_orderlines().length === 0 && this.currentOrder.is_to_invoice()) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Empty Order'),
                        body: this.env._t(
                            'There must be at least one product in your order before it can be validated and invoiced.'
                        ),
                    });
                    return false;
                }

                const splitPayments = this.paymentLines.filter(payment => payment.payment_method.split_transactions)
                if (splitPayments.length && !this.currentOrder.get_client()) {
                    const paymentMethod = splitPayments[0].payment_method
                    const {confirmed} = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Customer Required'),
                        body: _.str.sprintf(this.env._t('Customer is required for %s payment method.'), paymentMethod.name),
                    });
                    if (confirmed) {
                        this.selectClient();
                    }
                    return false;
                }

                if ((this.currentOrder.is_to_invoice() || this.currentOrder.is_to_ship()) && !this.currentOrder.get_client()) {
                    const {confirmed} = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Please select the Customer'),
                        body: this.env._t(
                            'You need to select the customer before you can invoice or ship an order.'
                        ),
                    });
                    if (confirmed) {
                        this.selectClient();
                    }
                    return false;
                }

                if (!this.currentOrder.get_total_with_tax()) {
                    const {confirmed} = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Please check the price .'),
                        body: this.env._t(
                            'You need to add price before you can invoice or ship an order.'
                        ),
                    });
                    if (confirmed) {
                        this.showScreen('ProductScreen');

                    }
                    return false;
                }
                for (let id in this.currentOrder.get_orderlines()) {
                    if (!this.currentOrder.get_orderlines()[id].salesperson) {
                        const {confirmed} = await this.showPopup('ConfirmPopup', {
                            title: this.env._t('Please check the salesperson .'),
                            body: this.env._t(
                                'You need to add salesperson for all items before you can invoice or ship an order.'
                            ),
                        });
                        if (confirmed) {
                            this.showScreen('ProductScreen');

                        }
                        return false;
                    }
                }

                var customer = this.currentOrder.get_client()
                if (this.currentOrder.is_to_ship() && !(customer.name && customer.street && customer.city && customer.country_id)) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Incorrect address for shipping'),
                        body: this.env._t('The selected customer needs an address.'),
                    });
                    return false;
                }

                if (!this.currentOrder.is_paid() || this.invoicing) {
                    return false;
                }

                if (this.currentOrder.has_not_valid_rounding()) {
                    var line = this.currentOrder.has_not_valid_rounding();
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Incorrect rounding'),
                        body: this.env._t(
                            'You have to round your payments lines.' + line.amount + ' is not rounded.'
                        ),
                    });
                    return false;
                }

                // The exact amount must be paid if there is no cash payment method defined.
                if (
                    Math.abs(
                        this.currentOrder.get_total_with_tax() - this.currentOrder.get_total_paid() + this.currentOrder.get_rounding_applied()
                    ) > 0.00001
                ) {
                    var cash = false;
                    for (var i = 0; i < this.env.pos.payment_methods.length; i++) {
                        cash = cash || this.env.pos.payment_methods[i].is_cash_count;
                    }
                    if (!cash) {
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Cannot return change without a cash payment method'),
                            body: this.env._t(
                                'There is no cash payment method available in this point of sale to handle the change.\n\n Please pay the exact amount or add a cash payment method in the point of sale configuration'
                            ),
                        });
                        return false;
                    }
                }

                // if the change is too large, it's probably an input error, make the user confirm.
                if (
                    !isForceValidate &&
                    this.currentOrder.get_total_with_tax() > 0 &&
                    this.currentOrder.get_total_with_tax() * 1000 < this.currentOrder.get_total_paid()
                ) {
                    this.showPopup('ConfirmPopup', {
                        title: this.env._t('Please Confirm Large Amount'),
                        body:
                            this.env._t('Are you sure that the customer wants to  pay') +
                            ' ' +
                            this.env.pos.format_currency(this.currentOrder.get_total_paid()) +
                            ' ' +
                            this.env._t('for an order of') +
                            ' ' +
                            this.env.pos.format_currency(this.currentOrder.get_total_with_tax()) +
                            ' ' +
                            this.env._t('? Clicking "Confirm" will validate the payment.'),
                    }).then(({confirmed}) => {
                        if (confirmed) this.validateOrder(true);
                    });
                    return false;
                }

                if (!this._isValidEmptyOrder()) return false;

                return true;
            }

            // IsCustomButton() {
            //     // click_invoice
            //     Gui.showPopup("ErrorPopup", {
            //         title: this.env._t('Payment Screen Custom Button Clicked'),
            //         body: this.env._t('Welcome to OWL'),
            //     });
            // }
        };
    Registries.Component.extend(PaymentScreen, CustomButtonPaymentScreen);
    return CustomButtonPaymentScreen;
});