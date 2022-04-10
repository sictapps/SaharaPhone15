odoo.define('sapps_pos_select_product_by_serial.pointOfSaleModelInherited', function (require) {
    'use strict';
    const models = require('point_of_sale.models');
    var core = require('web.core');
    var { Gui } = require('point_of_sale.Gui');
    var rpc = require('web.rpc')
    var _t = core._t;
    var super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        //@Override
        add_product(product, options) {
            if(options["draftPackLotLines"] !== undefined && (options["draftPackLotLines"]["newPackLotLines"] || options["draftPackLotLines"]["modifiedPackLotLines"])){
                //check if lot exist
                var new_lots = [];
                var modified_lots = [];
                if(options["draftPackLotLines"]["newPackLotLines"]){
                    new_lots = options["draftPackLotLines"]["newPackLotLines"].map((elem) => {return elem["lot_name"]});
                }
                if(options["draftPackLotLines"]["modifiedPackLotLines"]){
                    for (var key in options["draftPackLotLines"]["modifiedPackLotLines"]){
                        if(options["draftPackLotLines"]["modifiedPackLotLines"][key].length){
                            modified_lots.push(options["draftPackLotLines"]["modifiedPackLotLines"][key]);
                        }
                    }
                }

                var lots = new_lots.concat(modified_lots);
                    var self = this;
                    var args = arguments;
                    rpc.query({
                        model: 'stock.production.lot',
                        method: 'search',
                        args:  [[['name', 'in', lots]]]
                    }).then(function (backend_result) {
                        debugger;
                        var foundProductIds = backend_result
                        if(foundProductIds.length == lots.length){
                            var prod = rpc.query({
                                model: 'stock.production.lot',
                                method: 'check_if_lot_exists',
                                args: [foundProductIds[0], lots],
                            }).then(function (res){
                                var prod = res;
                                prod.forEach((lt) => {
                                    if(lt.quantity <= 0 )
                                    {
                                        return Gui.showPopup('OfflineErrorPopup', {
                                            title: _t('Serial Error'),
                                            body: _t("Serial have no quantity in stock - " + lt.lot),
                                        });
                                    }
                                });
                                return super_order.add_product.apply(self, args);

                            }).catch(function (data) {
                                return Gui.showPopup('OfflineErrorPopup', {
                                        title: _t('Connection Error'),
                                        body: _t("Connection Error, please try again"),
                                    });
                            });

                        }else if(foundProductIds.length > lots.length){
                            return Gui.showPopup('OfflineErrorPopup', {
                                title: _t('Serial Error'),
                                body: _t("Duplicated serial in stock"),
                            });
                        }else{
                            return Gui.showPopup('OfflineErrorPopup', {
                                title: _t('Serial Error'),
                                body: _t("Serial not found in stock"),
                            });
                        }
                }).catch(function (data) {
                    return Gui.showPopup('OfflineErrorPopup', {
                        title: _t('Connection Error'),
                        body: _t("Connection Error, please try again"),
                    });
                });
            }else{
                return super_order.add_product.apply(this, arguments);
            }
        },
    });
});