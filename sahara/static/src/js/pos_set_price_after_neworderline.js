
odoo.define('sahara.possetpriceafterneworderline', function(require) {
    'use strict';
       const Registries = require('point_of_sale.Registries');
       const ProductScreen = require('point_of_sale.ProductScreen');
       const NumberBuffer = require('point_of_sale.NumberBuffer');
        const possetpriceafterneworderline = (ProductScreen) =>
           class extends ProductScreen {
               constructor() {
                super(...arguments);
               }
            _newOrderlineSelected() {
                // console.log('bbbbbbb');
                self = this;
                setTimeout(() => {
                    NumberBuffer.reset();
                    self.state.numpadMode = 'price';
                }, 200); 
            }
           };
       Registries.Component.extend(ProductScreen, possetpriceafterneworderline);
       return possetpriceafterneworderline;
    });