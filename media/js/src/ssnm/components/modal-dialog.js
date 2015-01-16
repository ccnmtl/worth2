(function() {
    'use strict';

    Ssnm.ModalDialogComponent = Em.Component.extend({
        actions: {
            // This is required for the closeModal action to get through
            // to the ApplicationRoute.
            closeModal: function() {
                return this.sendAction();
            }
        }
    });
})();
