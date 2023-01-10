odoo.define('sahara_planet.SendAndRefund', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var rpc = require('web.rpc');


    var posModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        send_invoice() {
            var result = rpc.query({
                model: 'pos.order',
                method: 'send_order_pos',
                args: [[]],
            }).then(function (result2) {
                try {
                   if (result2.startsWith("Could not issue tax refund")) {
                    alert(result2)//Stop instructions here;
                } else if (result2.startsWith("Tax-Free tag successfully")) {
                    alert(result2) //continue to work;
                }else if (result2.startsWith("Tag has been voided")) {
                    alert(result2) //continue to work;
                }else if (result2.startsWith("Can't void tag")) {
                    alert(result2) //continue to work;
                }else if (result2.startsWith("Transaction does not exist")) {
                    alert(result2) //continue to work;
                }else if (result2) {
                    alert(result2)
                    //continue to work;
                }
                }catch (e) {

                }

            });
        },


        edit_tag_number() {
            this.rpc({
                model: 'pos.order',
                method: 'get_tag',
                args: [[]],


            });
        },

        push_and_invoice_order: function (order) {
            var self = this;
            return new Promise((resolve, reject) => {
                if (!order.get_client()) {
                    reject({code: 400, message: 'Missing Customer', data: {}});
                } else {

                    var order_id = self.db.add_order(order.export_as_JSON());



                    self.flush_mutex.exec(async () => {


                        try {

                            const server_ids = await self._flush_orders([self.db.get_order(order_id)], {
                                timeout: 30000,
                                to_invoice: true,
                            });
                            try {
                                this.send_invoice()
                            }catch (e) {

                            }





                            if (server_ids.length) {

                                const [orderWithInvoice] = await self.rpc({
                                    method: 'read',
                                    model: 'pos.order',
                                    args: [server_ids, ['account_move']],
                                    kwargs: {load: false},
                                });

                                await self
                                    .do_action('account.account_invoices', {
                                        additional_context: {
                                            active_ids: [orderWithInvoice.account_move],
                                        },
                                    })
                                    .catch(() => {
                                        reject({code: 401, message: 'Backend Invoice', data: {order: order}});

                                    });

                            } else {
                                reject({code: 401, message: 'Backend Invoice', data: {order: order}});
                            }
                            resolve(server_ids);
                        } catch (error) {
                            reject(error);
                        }
                    });
                }
            });
        },
    });

});
