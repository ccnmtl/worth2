(function() {
    'use strict';

    /**
     * controller:supporters
     *
     * This is the main application controller (it handles the
     * ApplicationRoute). All it needs to do is put the supporters in 3
     * different arrays based on closeness.
     */
    Ssnm.SupportersController = Em.ArrayController.extend({
        itemController: 'supporter',

        veryCloseSupporters: Em.computed.filterBy('model', 'closeness', 'VC'),
        closeSupporters: Em.computed.filterBy('model', 'closeness', 'C'),
        notCloseSupporters: Em.computed.filterBy('model', 'closeness', 'NC')
    });
})();
