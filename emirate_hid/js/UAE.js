

odoo.define('EmirateHID.Read', function (require) {
    'use strict';

var core = require('web.core');
var Widget = require('web.Widget');
var field_registry = require('web.field_registry');
var widget_registry = require('web.widget_registry');
var Dialog = require('web.Dialog');
var basic_fields = require('web.basic_fields');
var FormRenderer = require('web.FormRenderer');
var FormView = require('web.FormView');
var viewRegistry = require('web.view_registry');
var AbstractField = require('web.AbstractField');

var field_utils = require('web.field_utils');

var QWeb = core.qweb;
var _t = core._t;



var UAEFormRenderer = FormRenderer.extend({
    events: _.extend({}, FormRenderer.prototype.events, {
        "click .btn-readCard": "_callExtenion",
        "click .simulateEidResponse": "_getdata"
    }),
    /*
     * Open the m2o item selection from another button
     */
       _callExtenion: function (event) {
        var event = document.createEvent('Event');
          event.initEvent('EID_EVENT');
          document.dispatchEvent(event);
         // document.getElementById("simulateEidResponse").style.display = "none";




    },

    _getdata: function (event) {
     event.preventDefault();
        var self = this;
          var response = this.$('.simulateEidResponse').text();
          if (response.length >10)
          {
          var jsondata = $.parseJSON(response);
          let le=document.getElementsByName('jsondata')[0];
          le.value=response;
          var event = new Event('change');
          le.dispatchEvent(event);
          }



         // self.fieldIdsToNames.simulateEidResponse =jsondata;




    },
});

var Read = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Renderer: UAEFormRenderer,
    }),
});

viewRegistry.add("UAE", Read);

    return Read;


});
