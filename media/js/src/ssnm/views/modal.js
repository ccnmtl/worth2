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
        },
        keyDown: function(e) {
            Em.debug('view:modal keyDown');
            if (e.keyCode === 13 && !Em.$(e.target).hasClass('btn')) {
                // The user pressed Enter.
                return false;
            } else if (e.keyCode === 27) {
                // The user pressed Escape.
                Em.debug('view:keyDown sending closeModal');
                this.get('controller').send('closeModal');
                return false;
            }
        }
    });
})();
