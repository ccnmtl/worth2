(function() {
    'use strict';

    Ssnm.SupporterController = Em.ObjectController.extend({
        actions: {
            editSupporter: function() {
                Em.debug('editSupporter: ' + this.get('name'));
            }
        }
    });
})();
