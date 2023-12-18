odoo.define('EmirateHID.Read', function (require) {
    'use strict';

    var core = require('web.core');
    var FormRenderer = require('web.FormRenderer');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');

    var QWeb = core.qweb;
    var _t = core._t;

    var UAEFormRenderer = FormRenderer.extend({
            events: _.extend({}, FormRenderer.prototype.events, {
                "click .btn-readCard": "_callExtension",
                "click .simulateEidResponse": "_getData"
            }),

            _callExtension: function (event) {
                var customEvent = new Event('EID_EVENT');
                document.dispatchEvent(customEvent);
            },

            _getData: function (event) {
                event.preventDefault();
                var self = this;
                var simulateEidResponseField = this.$('.simulateEidResponse');

                if (simulateEidResponseField.length > 0) {
                    var response = simulateEidResponseField.text();

                    if (response.length > 10) {
                        try {
                            var jsonData = JSON.parse(response);
                            var jsonField = this.$('input[name="jsondata"]');
                            jsonField.val(response).change();  // Trigger the change event
                        } catch (error) {
                            console.error('Error parsing JSON:', error);
                            // Handle the error as needed
                        }
                    }
                }
            },
        })
    ;

    var Read = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Renderer: UAEFormRenderer,
        }),
    });

    viewRegistry.add("UAE", Read);

    return Read;
});
