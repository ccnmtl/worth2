/* global Ember */

(function() {
    'use strict';

    Ember.Handlebars.helper('influenceColorClass', function(value, options) {
        var influence = Ember.Handlebars.Utils.escapeExpression(value);

        var str = '';
        if (influence === 'P') {
            str = 'ssnm-color-positive';
        } else if (influence === 'MP') {
            str =  'ssnm-color-mostly-positive';
        } else if (influence === 'MN') {
            str = 'ssnm-color-mostly-negative';
        } else if (influence === 'N') {
            str = 'ssnm-color-negative';
        }

        return str;
    });
})();
