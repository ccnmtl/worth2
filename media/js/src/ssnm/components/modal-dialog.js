(function() {
    'use strict';

    Ssnm.ModalDialogComponent = Em.Component.extend({
        actions: {
            closeModal: function() {
                return this.sendAction();
            }
        }
    });
})();
