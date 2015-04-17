(function() {
    'use strict';

    /**
     * controller:supporters
     *
     * This is the main application controller (it handles the
     * ApplicationRoute).
     */
    Ssnm.SupportersController = Em.ArrayController.extend({
        needs: ['edit-supporter'],
        itemController: 'supporter',

        // An array of all supporters in the system that have been loaded
        // from the back-end. This excludes the temporary supporter that
        // exists only on the front-end, during the series of modals after
        // clicking "Add People".
        savedSupporters: Em.computed.filter('model', function(supporter) {
            return !supporter.get('isNew');
        }).property('model.@each.isNew'),

        veryCloseSupporters: Em.computed.filterBy(
            'savedSupporters', 'closeness', 'VC'),
        closeSupporters: Em.computed.filterBy(
            'savedSupporters', 'closeness', 'C'),
        notCloseSupporters: Em.computed.filterBy(
            'savedSupporters', 'closeness', 'NC'),

        actions: {
            addSupporter: function() {
                Em.debug('controller:supporters addSupporter');
                if (this.get('savedSupporters.length') < 5) {
                    var editSupporterController = this.get(
                        'controllers.edit-supporter');
                    editSupporterController.setProperties({
                        'isEditing': false,
                        'model': this.store.createRecord('supporter')
                    });
                    this.send('openModal', 'edit-supporter-modal-1');
                } else {
                    Em.debug('Max supporters!');
                    this.send('openModal', 'max-supporters-modal');
                }
            },

            /**
             * This action occurs when a participant clicks on one of
             * their existing supporters in the social support network
             * map.
             */
            editSupporter: function(supporter) {
                Em.debug('controller:supporters editSupporter');
                var editSupporterController = this.get(
                    'controllers.edit-supporter');
                editSupporterController.setProperties({
                    'isEditing': true,
                    'model': supporter
                });
                this.send('openModal', 'edit-supporter-modal-1');
            }
        }
    });
})();
