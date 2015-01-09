(function() {
    'use strict';

    Ssnm.ModalView = Em.View.extend({
        click: function(e) {
            // If the user clicked on the shaded modal backdrop, close the
            // window.
            if (Em.$(e.target).hasClass('roulette-modal')) {
                return this.get('controller').send('closeModal');
            }
        }
    });
})();
