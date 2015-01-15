(function() {
    'use strict';

    Ssnm.ModalView = Em.View.extend({
        click: function(e) {
            Em.debug('view:modal click');
            // If the user clicked on the shaded modal backdrop, close the
            // window.
            if (Em.$(e.target).hasClass('ssnm-modal')) {
                Em.debug('view:modal sending closeModal');
                this.get('controller').send('closeModal');
            }
        }
    });
})();
