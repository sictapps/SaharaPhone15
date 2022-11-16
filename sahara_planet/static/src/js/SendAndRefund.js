odoo.define('sahara_planet.Tax', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');

    const MPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
            }

            send_invoice() {
                rpc.query({
                    model: 'pos.order',
                    method: 'send_order_pos',
                    args: [[]],


                });
            }

            refund_invoice() {

                rpc.query({
                    model: 'pos.order',
                    method: 'refund_order_pos',
                    args: [[]],


                });
            }

            async _finalizeValidation() {
                if ((this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change()) && this.env.pos.config.iface_cashdrawer) {
                    this.env.pos.proxy.printer.open_cashbox();
                }

                this.currentOrder.initialize_validation_date();
                this.currentOrder.finalized = true;

                let syncedOrderBackendIds = [];

                try {
                    if (this.currentOrder.is_to_invoice()) {
                        syncedOrderBackendIds = await this.env.pos.push_and_invoice_order(
                            this.currentOrder
                        );
                    } else {
                        syncedOrderBackendIds = await this.env.pos.push_single_order(this.currentOrder);
                    }
                } catch (error) {
                    if (error.code == 700)
                        this.error = true;

                    if ('code' in error) {
                        // We started putting `code` in the rejected object for invoicing error.
                        // We can continue with that convention such that when the error has `code`,
                        // then it is an error when invoicing. Besides, _handlePushOrderError was
                        // introduce to handle invoicing error logic.
                        await this._handlePushOrderError(error);
                    } else {
                        // We don't block for connection error. But we rethrow for any other errors.
                        if (isConnectionError(error)) {
                            this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Connection Error'),
                                body: this.env._t('Order is not synced. Check your internet connection'),
                            });
                        } else {
                            throw error;
                        }
                    }
                }
                if (syncedOrderBackendIds.length && this.currentOrder.wait_for_push_order()) {
                    const result = await this._postPushOrderResolve(
                        this.currentOrder,
                        syncedOrderBackendIds
                    );
                    if (!result) {
                        await this.showPopup('ErrorPopup', {
                            title: this.env._t('Error: no internet connection.'),
                            body: this.env._t('Some, if not all, post-processing after syncing order failed.'),
                        });
                    }
                }

                this.showScreen(this.nextScreen);

                // If we succeeded in syncing the current order, and
                // there are still other orders that are left unsynced,
                // we ask the user if he is willing to wait and sync them.
                if (syncedOrderBackendIds.length && this.env.pos.db.get_orders().length) {
                    const {confirmed} = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Remaining unsynced orders'),
                        body: this.env._t(
                            'There are unsynced orders. Do you want to sync these orders?'
                        ),
                    });
                    if (confirmed) {
                        // NOTE: Not yet sure if this should be awaited or not.
                        // If awaited, some operations like changing screen
                        // might not work.
                        this.env.pos.push_orders();
                    }
                }
            }

            get nextScreen() {
                console.log('55555555555555')
                this.send_invoice()
                this.refund_invoice()
                return !this.error ? 'ReceiptScreen' : 'ProductScreen';
            }


            // createMRP(){
            //     const order = this.currentOrder;
            // var order_line = order.orderlines.models;
            // var due = order.get_due();
            //  for (var i in order_line)
            //   {
            //      var list_product = []
            //      if (order_line[i].product.to_make_mrp)
            //      {
            //        if (order_line[i].quantity>0)
            //        {
            //          var product_dict = {
            //             'id': order_line[i].product.id,
            //             'qty': order_line[i].quantity,
            //             'product_tmpl_id': order_line[i].product.product_tmpl_id,
            //             'pos_reference': order.name,
            //             'uom_id': order_line[i].product.uom_id[0],
            //        };
            //       list_product.push(product_dict);
            //      }
            //
            //   }
            //
            //   if (list_product.length)
            //   {
            //     rpc.query({
            //         model: 'mrp.production',
            //         method: 'create_mrp_from_pos',
            //         args: [1,list_product],
            //         });
            //   }
            // }
            // }
            //     async validateOrder(isForceValidate) {
            //     if(this.env.pos.config.cash_rounding) {
            //         if(!this.env.pos.get_order().check_paymentlines_rounding()) {
            //             this.showPopup('ErrorPopup', {
            //                 title: this.env._t('Rounding error in payment lines'),
            //                 body: this.env._t("The amount of your payment lines must be rounded to validate the transaction."),
            //             });
            //             return;
            //         }
            //     }
            //     if (await this._isOrderValid(isForceValidate)) {
            //         // remove pending payments before finalizing the validation
            //         for (let line of this.paymentLines) {
            //             if (!line.is_done()) this.currentOrder.remove_paymentline(line);
            //         }
            //         await this._finalizeValidation();
            //     }
            //     this.createMRP();
            // }
        };

    Registries.Component.extend(PaymentScreen, MPaymentScreen);

    return MPaymentScreen;

});
