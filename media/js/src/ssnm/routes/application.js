(function() {
    'use strict';

    /**
     * route:application
     */
    Ssnm.ApplicationRoute = Em.Route.extend({
        controllerName: 'supporters',

        actions: {
            openModal: function(modalName) {
                Em.debug('route:application openModal');

                var controllerName = modalName;

                // Use the EditSupporterController when rendering any of
                // the EditSupporter modals.
                if (modalName.match(/edit-supporter-modal/)) {
                    controllerName = 'edit-supporter';
                }

                try {
                    // Attempt to render this view with a custom controller.
                    Em.debug('Rendering ' + modalName +
                             ' with controller ' + controllerName);
                    return this.render(modalName, {
                        into: 'application',
                        outlet: 'modal',
                        controller: controllerName
                    });
                } catch (e) {
                    // If the custom modal controller doesn't exist, the
                    // previous render statement throws an exception, and
                    // we use the base modal controller.
                    Em.debug('Fell back to default controller');
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
