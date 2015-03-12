define([
    'jquery',
    'underscore',
    'backbone',
], function($, _, Backbone) {
    var GoalSettingFormView = Backbone.View.extend({
        el: '#goal-setting-block',

        events: {
            change: 'change'
        },

        initialize: function() {
            if (this.$el.length === 0) {
                return;
            }

            $('.pagetree-form-submit-area input').hide();

            // Make an array containing a jQuery object for each form
            // in the formset.
            this.$forms = this.$el.find('.goal-form');
            this.refreshOtherInputDisplay(this.$forms);
        },

        change: function() {
            this.refreshOtherInputDisplay(this.$forms);
        },

        /**
         * This function looks at each form in the array '$forms' and
         * hides or shows the "Other" text input based on the state of
         * the form's dropdown option.
         */
        refreshOtherInputDisplay: function($forms) {
            $forms.each(function(k, v) {
                var $v = $(v);
                var $option = $v.find('select.goal-option');

                var $otherInput = $v.find('.other-text');
                var $otherForm = $otherInput.closest('.goal-other-container');

                var selectedLabel = $.trim(
                    $option.find('option:selected').text()).toLowerCase();

                if (selectedLabel === 'other') {
                    $otherForm.show();
                } else {
                    $otherInput.val('');
                    $otherForm.hide();
                }
            });
        }
    });

    return GoalSettingFormView;
});
