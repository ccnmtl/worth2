/* global Ember */
/*
 * From https://github.com/Blooie/ember-radio-buttons
 */

(function() {
    'use strict';

    Ssnm.RadioButtonView = Ember.View.extend({
        tagName: 'input',
        type: 'radio',
        attributeBindings: ['type', 'htmlChecked:checked', 'value', 'name'],

        htmlChecked: function() {
            return this.get('value') === this.get('checked');
        }.property('value', 'checked'),

        change: function() {
            this.set('checked', this.get('value'));
        },

        _updateElementValue: function() {
            Ember.run.next(this, function() {
                this.$().prop('checked', this.get('htmlChecked'));
            });
        }.observes('htmlChecked')
    });
})();
