odoo.define('sahara.setdefaultcustomer', function(require) {
    'use strict';
       const Registries = require('point_of_sale.Registries');
       const ProductScreen = require('point_of_sale.ProductScreen');
        const setdefaultcustomer = (ProductScreen) =>
           class extends ProductScreen {
               constructor() {
                super(...arguments);
               }
               mounted() {          
                self = this;
                setTimeout(() => {
                    var res = this.env.pos.db.search_partner('General Customer');
                    if(res[0]){
                        this.currentOrder.set_client(res[0]);
                        this.currentOrder.updatePricelist(res[0]);
                    }
                },400); 
                // console.log('aaaaaaaaaaa');
               }
           };
       Registries.Component.extend(ProductScreen, setdefaultcustomer);
       return setdefaultcustomer;
    });