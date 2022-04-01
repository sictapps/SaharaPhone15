odoo.define('sahara.possetPridceDefault', function(require) {
    'use strict';
       const Registries = require('point_of_sale.Registries');
       const NumpadWidget = require('point_of_sale.NumpadWidget');
        const possetPridceDefault = (NumpadWidget) =>
           class extends NumpadWidget {
               constructor() {
                super(...arguments);
               }
               mounted() {          
                const self2= this;
                setTimeout(() => {
                    self2.changeMode('price');
                },100); 
                // console.log('aaaaaaaaaaa');
               }
           };
       Registries.Component.extend(NumpadWidget, possetPridceDefault);
       return possetPridceDefault;
    });