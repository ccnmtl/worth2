(function() {
    'use strict';

    Ssnm.SupporterBoxComponent = Em.Component.extend({
        click: function() {
            Em.debug('component:supporter click');
            var supporter = this.get('supporter');
            return this.sendAction('clickedSupporter', supporter);
        }
    });
})();
