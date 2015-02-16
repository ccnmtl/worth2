(function() {
    'use strict';

    /**
     * controller:edit-supporter
     *
     * This controller handles the Supporter object created through the
     * "Add Supporter" dialogs.
     */
    Ssnm.EditSupporterController = Em.ObjectController.extend({
        title: function() {
            if (this.get('isEditing')) {
                return 'Making changes to ' + this.get('name');
            } else {
                return 'Add to your support network';
            }
        }.property('isEditing', 'name'),

        // Determines whether the user is adding a new supporter, or
        // editing an existing one.
        isEditing: false,

        hasBlankName: Em.computed.empty('name'),
        hasBlankCloseness: Em.computed.empty('closeness'),
        hasBlankInfluence: Em.computed.empty('influence'),

        actions: {
            deleteSupporter: function() {
                Em.debug('controller:edit-supporter deleteSupporter');

                var me = this;
                this.get('model').destroyRecord()
                    .then(function() {
                        me.send('closeModal');
                    });
            },
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
