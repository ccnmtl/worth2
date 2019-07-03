(function() {
    'use strict';

    Ssnm.SupporterBoxComponent = Em.Component.extend({
        click: function() {
            Em.debug('component:supporter click');
            var supporter = this.get('supporter');
            return this.sendAction('clickedSupporter', supporter);
        },
        keyDown: function(evt) {
            if (evt.keyCode === 13) {
                Em.debug('component:supporter enter');
                var supporter = this.get('supporter');
                return this.sendAction('clickedSupporter', supporter);
            }
        }
    });
})();
