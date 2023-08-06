odoo.define('new_sahara.OrderWidget', function (require) {
        'use strict';

        const OrderWidget = require('point_of_sale.OrderWidget');
        const Registries = require('point_of_sale.Registries');
        const {useState, useRef, onPatched} = owl.hooks;

        const RetailOrderWidget = (OrderWidget) =>
            class extends OrderWidget {
                constructor() {
                    super(...arguments);
                    this.state = useState({
                        total: 0,
                        tax: 0,
                        discount: 0,
                        totalWithOutTaxes: 0,
                        margin: 0,
                        totalItems: 0,
                        totalQuantities: 0,
                    });
                }

                _selectLine(event) {
                    super._selectLine(event)
                }

                async _editPackLotLines(event) {
                    const orderline = event.detail.orderline;
                    console.log(orderline, 'orderline');
                    const isAllowOnlyOneLot = orderline.product.isAllowOnlyOneLot();
                    const packLotLinesToEdit = orderline.getPackLotLinesToEdit(isAllowOnlyOneLot);
                    const {confirmed, payload} = await this.showPopup('EditListPopup', {
                        title: this.env._t('Lot/Serial Number(s) Required'),
                        isSingleItem: isAllowOnlyOneLot,
                        array: packLotLinesToEdit,
                    });
                    if (confirmed) {
                        // Segregate the old and new packlot lines
                        const modifiedPackLotLines = Object.fromEntries(
                            payload.newArray.filter(item => item.id).map(item => [item.id, item.text])
                        );

                        const newPackLotLines = payload.newArray
                            .filter(item => !item.id)
                            .map(item => ({lot_name: item.text}));

                        // Iterate through each entry in this.env.pos.toRefundLines
                        for (const key in this.env.pos.toRefundLines) {
                            const refundLine = this.env.pos.toRefundLines[key];
                            if (refundLine.destinationOrderUid !== false) {
                                const orderlineToRefund = refundLine.orderline;

                                // Search for the serial number in the original sales order
                                const orderToRefundId = orderlineToRefund.orderBackendId;
                                const orderToRefund = await this.env.pos.rpc({
                                    model: 'pos.order',
                                    method: 'search_read',
                                    domain: [['id', '=', orderToRefundId]],
                                    fields: ['lines', 'name', 'partner_id', 'date_order'],
                                    limit: 1,
                                });

                                const lineIds = orderToRefund[0].lines;
                                const lines = await this.env.pos.rpc({
                                    model: 'pos.order.line',
                                    method: 'search_read',
                                    domain: [['id', 'in', lineIds]],
                                });
                                let originalOrderline = null;
                                for (let i = 0; i < lines.length; i++) {
                                    const line = lines[i];
                                    const lotIds = line.pack_lot_ids;
                                    const lot_id = await this.env.pos.rpc({
                                        model: 'pos.pack.operation.lot',
                                        method: 'search_read',
                                        domain: [['id', 'in', lotIds]],
                                    });
                                    console.log('lot_id', lot_id);
                                    originalOrderline = lot_id.find(lot => {
                                        return (
                                            lot.product_id[0] === orderline.product.id &&
                                            newPackLotLines[0] &&
                                            lot.lot_name === newPackLotLines[0].lot_name
                                        );
                                    });
                                    if (originalOrderline) {
                                        break;
                                    }
                                }

                                if (!originalOrderline) {
                                    this.showPopup('ErrorPopup', {
                                        title: this.env._t('Serial Number Error'),
                                        body: this.env._t('The serial number entered does not match the one in the original sales order.'),
                                    });
                                    return;
                                }

                                orderline.setPackLotLines({modifiedPackLotLines, newPackLotLines});
                            } else {
                                console.log(`destinationOrderUid is false for entry ${key}. Cannot proceed with the refund.`);
                            }
                        }
                    }
                    this.order.select_orderline(event.detail.orderline);
                }
            }

        Registries.Component.extend(OrderWidget, RetailOrderWidget);

        return RetailOrderWidget;
    }
);
