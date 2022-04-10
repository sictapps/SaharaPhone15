odoo.define('sapps_pos_select_product_by_serial.ProductScreenInherited', function(require) {
    'use strict';
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');
    const ControlWidget = require("point_of_sale.ProductsWidgetControlPanel");
    const ByLotProductScreen = (ProductScreen) =>
        class extends ProductScreen{

        async _byLotGetAddProductOptions(product, base_code, serial) {
            let price_extra = 0.0;
            let draftPackLotLines, weight, description, packLotLinesToEdit;

            if (this.env.pos.config.product_configurator && _.some(product.attribute_line_ids, (id) => id in this.env.pos.attributes_by_ptal_id)) {
                let attributes = _.map(product.attribute_line_ids, (id) => this.env.pos.attributes_by_ptal_id[id])
                                  .filter((attr) => attr !== undefined);
                let { confirmed, payload } = await this.showPopup('ProductConfiguratorPopup', {
                    product: product,
                    attributes: attributes,
                });

                if (confirmed) {
                    description = payload.selected_attributes.join(', ');
                    price_extra += payload.price_extra;
                } else {
                    return;
                }
            }

            // Gather lot information if required.
            if (['serial', 'lot'].includes(product.tracking) && (this.env.pos.picking_type.use_create_lots || this.env.pos.picking_type.use_existing_lots)) {
                const isAllowOnlyOneLot = product.isAllowOnlyOneLot();
                if (isAllowOnlyOneLot) {
                    packLotLinesToEdit = [];
                } else {
                    const orderline = this.currentOrder
                        .get_orderlines()
                        .filter(line => !line.get_discount())
                        .find(line => line.product.id === product.id);
                    if (orderline) {
                        packLotLinesToEdit = orderline.getPackLotLinesToEdit();
                    } else {
                        packLotLinesToEdit = [];
                    }
                }
                const modifiedPackLotLines = {};
                packLotLinesToEdit.forEach((elem) => {
                    modifiedPackLotLines[elem.id] = elem.text;
                });
                const newPackLotLines = [{"lot_name": serial}];
                draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
            }

            // Take the weight if necessary.
            if (product.to_weight && this.env.pos.config.iface_electronic_scale) {
                // Show the ScaleScreen to weigh the product.
                if (this.isScaleAvailable) {
                    const { confirmed, payload } = await this.showTempScreen('ScaleScreen', {
                        product,
                    });
                    if (confirmed) {
                        weight = payload.weight;
                    } else {
                        // do not add the product;
                        return;
                    }
                } else {
                    await this._onScaleNotAvailable();
                }
            }

//            if (base_code && this.env.pos.db.product_packaging_by_barcode[base_code.code]) {
//                weight = this.env.pos.db.product_packaging_by_barcode[base_code.code].qty;
//            }

            return { draftPackLotLines, quantity: weight, description, price_extra };
        }
        /*
         * @override
        */
        async _barcodeProductAction(code) {
            debugger;
            let foundProductIds = [];
                try {
                    foundProductIds = await this.rpc({
                        model: 'stock.production.lot',
                        method: 'custom_search',
                        args: [1, [code.base_code]],
                        context: this.env.session.user_context,
                    });
                } catch (error) {
                    if (isConnectionError(error)) {
                        return this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Network Error'),
                            body: this.env._t("Product is not loaded. Tried loading the product from the server but there is a network error."),
                        });
                    } else {
                        throw error;
                    }
                }
                if (foundProductIds.length == 1) {
                    try {
                        debugger;
                        var back_res = await this.rpc({
                            model: 'stock.production.lot',
                            method: 'check_if_lot_exists',
                            args: [foundProductIds[0], [code.base_code]],
                            context: this.env.session.user_context,
                        });
                        var prod = back_res[0];
                        if(prod.quantity > 0){
                            await this.env.pos._addProducts(prod.product_id);
                            // assume that the result is unique.
                            //product = this.env.pos.db.get_product_by_id(foundProductIds[0]);
                        }else{
                            return this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Serial Error'),
                                body: this.env._t("Serial have no quantity in stock"),
                            });
                        }
                    } catch (error) {
                        if (isConnectionError(error)) {
                            return this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Network Error'),
                                body: this.env._t("Product is not loaded. Tried loading the product from the server but there is a network error."),
                            });
                        } else {
                            throw error;
                        }
                    }
                } else if (foundProductIds.length > 1){
                    return this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Serial Error'),
                            body: this.env._t("Duplicated serial in stock"),
                        });

                }else{
                    return this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Serial Error'),
                            body: this.env._t("Serial not found in stock"),
                        });
                }
            $(".search-bar-portal > .search-box input[type='text']").val(prod.name);
            //$(".search-bar-portal > .search-box input[type='text']").trigger( "click" );
            ControlWidget.current.trigger('update-search', prod.name);
            let product = this.env.pos.db.get_product_by_id(prod.product_id);
            //let product = this.env.pos.db.get_product_by_barcode(code.base_code);
            const options = await this._byLotGetAddProductOptions(product, code, code.base_code);
            for (const [key, value] of Object.entries(options["draftPackLotLines"]["modifiedPackLotLines"])) {
                if (value.toLowerCase() == code.base_code.toLowerCase()){
                    return this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Serial Error'),
                                body: this.env._t("Already exist in your order"),
                            });
                }
            }
            this.currentOrder.add_product(product,  options)
        }
    }

    Registries.Component.extend(ProductScreen, ByLotProductScreen);
    return ProductScreen;
});
