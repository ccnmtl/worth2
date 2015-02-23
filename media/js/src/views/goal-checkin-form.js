define([
    'jquery',
    'underscore',
    'backbone',
], function($, _, Backbone) {
    var GoalCheckinFormView = Backbone.View.extend({
        el: '#goal-checkin-block',

        events: {
            change: 'change'
        },

        initialize: function() {
            if (this.$el.length === 0) {
                return;
            }

            // Make an array containing a jQuery object for each form
            // in the formset.
            this.$forms = this.$el.find('.checkin-group');
            this.refreshInputDisplay(this.$forms);
        },

        change: function() {
            this.refreshInputDisplay(this.$forms);
        },

        /**
         * This function looks at each form in the array '$forms' and
         * hides or shows the "What got in the way?" dropdown based on
         * the state of the form's "How did it go?" radio buttons.
         *
         * Additionally, based on whether the user selected the "Other"
         * option from the "What got in the way" dropdown, this function
         * shows or hides an "Other" text input below that dropdown.
         */
        refreshInputDisplay: function($forms) {
            $forms.each(function(k, v) {
                var $v = $(v);
                var $option = $v.find('input.how-it-went:checked');
                var optionVal = $option.val();
                var $whatGotInTheWayInput = $v.find(
                    'select.what-got-in-the-way');

                var $otherInput = $v.find('input.goal-checkin-other');

                if (!optionVal || optionVal === 'yes') {
                    $whatGotInTheWayInput.closest('.form-group').hide();
                    $otherInput.closest('.form-group').hide();
                } else if (optionVal === 'in progress' || optionVal === 'no') {
                    $whatGotInTheWayInput.closest('.form-group').show();

                    var whatGotInTheWayText = $.trim($whatGotInTheWayInput.find(
                        'option:selected').text()).toLowerCase();
                    if (whatGotInTheWayText === 'other') {
                        $otherInput.closest('.form-group').show();
                    } else {
                        $otherInput.closest('.form-group').hide();
                    }

                }
            });
        }
    });

    return GoalCheckinFormView;
});
