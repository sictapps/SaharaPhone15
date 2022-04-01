
odoo.define('sahara.possetpriceafterneworderline', function(require) {
    'use strict';
       const Registries = require('point_of_sale.Registries');
       const ProductScreen = require('point_of_sale.ProductScreen');
        const possetpriceafterneworderline = (ProductScreen) =>
           class extends ProductScreen {
               constructor() {
                super(...arguments);
               }
            _newOrderlineSelected() {
                // console.log('bbbbbbb');
                self = this;
                setTimeout(() => {
                    self.state.numpadMode = 'price';
                }, 200); 
            }
           };
       Registries.Component.extend(ProductScreen, possetpriceafterneworderline);
       return possetpriceafterneworderline;
    });