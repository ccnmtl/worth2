(function() {
    'use strict';

    Ssnm.SupportersController = Em.ArrayController.extend({
        itemController: 'supporter',

        veryCloseSupporters: Em.computed.filter('model', function(supporter) {
            return supporter.get('closeness') === 'VC';
        }).property('model.@each.closeness'),

        closeSupporters: Em.computed.filter('model', function(supporter) {
            return supporter.get('closeness') === 'C';
        }).property('model.@each.closeness'),

        notCloseSupporters: Em.computed.filter('model', function(supporter) {
            return supporter.get('closeness') === 'NC';
        }).property('model.@each.closeness')
    });
})();
