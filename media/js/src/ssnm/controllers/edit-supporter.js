(function() {
    'use strict';

    /**
     * controller:edit-supporter
     *
     * This controller handles the Supporter object created through the
     * "Add Supporter" dialogs.
     */
    Ssnm.EditSupporterController = Em.ObjectController.extend({
        title: 'Add to your support network',

        hasBlankName: Em.computed.empty('name'),
        hasBlankCloseness: Em.computed.empty('closeness'),
        hasBlankInfluence: Em.computed.empty('influence'),

        actions: {
            saveEditedSupporter: function() {
                Em.debug('controller:edit-supporter saveEditedSupporter');

                var me = this;
                this.get('model').save()
                    .then(function() {
                        me.send('closeModal');
                        me.set('model', me.store.createRecord('supporter'));
                    });
            }
        },

        model: function() {
            return this.store.createRecord('supporter');
        }.property()
    });
})();
