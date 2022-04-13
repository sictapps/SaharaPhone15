/* global Backbone, waitForWebfonts */
odoo.define('pos_orderline_salesperson.employeemodels', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var _super_posmodel = models.PosModel.prototype;
    var rpc = require('web.rpc')
    models.PosModel = models.PosModel.extend({
        // models:[{
        //     model:  'hr.employee',
        //         fields: ['name', 'id'],
        //         // domain: function(self){ return [] },
        //         loaded: function(self,employees){
        //             self.employees = employees;
        //             console.log(self.employees)
        //         },
        // }],
        initialize: function (session, attributes) {
            var self = this;
            // some new code in this method
            // models.load_fields('product.product',['credit_product']);
            // call original method via "apply"
            _super_posmodel.initialize.apply(this, arguments);
            this.models.push({
                // load allowed users
                         model:  'hr.employee',
                        fields: ['name', 'id'],
                        // domain: function(self){ return [] },
                        loaded: function(self,employees){
                            self.employees = employees;
                            console.log(self.employees)
                        },
                })
                return this;
             
            // console.log("in extended1");
            // // console.log(this.users);
            // // console.log(this.employee);
            // self.employees =  {
            //     model:  'hr.employee',
            //     fields: ['name', 'id'],
            //     // domain: function(self){ return [] },
            //     loaded: function(self,employees){
            //         self.employees = [employees];
            //         console.log(self.employees)
            //     },
            // };
            // console.log("in extended2");
            // console.log(self.employees)
        },
        after_load_server_data: async function() {
            var self = this;
            var res = await _super_posmodel.after_load_server_data.call(this);
                console.log("in extended7");
                console.log(this.users);
                console.log(this.employees);
                // this.employees =  {
                // model:  'hr.employee',
                // fields: ['name', 'id'],
                // // domain: function(self){ return [] },
                // loaded: function(self,employees){
                //     self.employees = [employees];
                //     return employees;
                //     },
                // };
                // console.log(2);
                //  rpc.query({
                //     model: 'hr.employee',
                //     method: 'read',
                //  }).then(function(res){
                //     console.log(1);
                //     this.employees = res;
                // })
                // this.employees = rpc.query({model: 'hr.employee', method: 'read', args: []})
                // .then(function (backend_result) {
                //     this.employees = backend_result;
                //     return this.employees;
                // });
             console.log("after load data")
             console.log(this.employees)
            return res;
        },
    
        // after_load_server_data: function () {
        //     var self = this;
        //     return _super_posmodel.after_load_server_data().then(function(){
        //         // var response = _super_posmodel.after_load_server_data();
        //         console.log("in extended7");
        //         console.log(this.users);
        //         console.log(this.employees);
        //         this.employees =  {
        //         model:  'hr.employee',
        //         fields: ['name', 'id'],
        //         // domain: function(self){ return [] },
        //         loaded: function(self,employees){
        //             self.employees = [employees];
        //             console.log(self.employees)
        //             },
        //         };
        //      console.log("after load data")
        //      console.log(this.employees)
            
        //     });
              
        // },
        // load_server_data: function(){
        //     var self = this;
        //     _super_posmodel.load_server_data();
        //     console.log("in extended1");
        //     console.log(this.users);
        //     console.log(this.employee);
        // }
    });

   
    
    });
    