(function() {
    'use strict';

    Ssnm.ApplicationRoute = Em.Route.extend({
        controllerName: 'supporters',

        actions: {
            openModal: function(modalName) {
                Em.debug('route:application openModal');
                try {
                    // Attempt to render this view with a custom controller.
                    return this.render(modalName, {
                        into: 'application',
                        outlet: 'modal',
                        controller: modalName
                    });
                } catch (e) {
                    // If the custom modal controller doesn't exist, the previous
                    // render statement throws an exception, and we use the base
                    // modal controller.
                    return this.render(modalName, {
                        into: 'application',
                        outlet: 'modal'
                    });
                }
            },
            closeModal: function() {
                Em.debug('route:application closeModal');
                return this.disconnectOutlet({
                    outlet: 'modal',
                    parentView: 'application'
                });
            }
        },

        model: function() {
            // Return all the supporters. The back-end will only return
            // supporters that belong to the logged-in participant.
            return this.store.find('supporter');
        }
    });
})();
