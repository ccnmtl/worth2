define([
    'jquery',
    'underscore',
    'backbone',
], function($, _, Backbone) {
    var SignInParticipantView = Backbone.View.extend({
        el: 'select#id_filter_by_cohort',
        events: {
            change: 'change'
        },

        /**
         * Update the participants displayed in the "Participant ID #"
         * dropdown based on the input number "val".
         */
        _updateDisplayedParticipants: function(filterVal) {
            var me = this;
            this.$targetInput.empty();

            this.$allOptions.each(function(k, v) {
                var $v = $(v);

                // Always append the top "Choose a Participant" option
                var text = $.trim($v.text()).toLowerCase();
                var cohortId = String($v.data('cohort-id'));
                if (
                    text === 'choose a participant' ||
                        'all' === filterVal ||
                        cohortId === filterVal
                ) {
                    me.$targetInput.append($v.clone(true));
                } else {
                    var val = $v.val();
                    me.$targetInput.find(
                        'option [value="' + val + '"]').remove();
                }
            });
            this.$options = this.$targetInput.find('option');
        },

        initialize: function() {
            if ($('.worth-facilitator-sign-in-participant').length !== 1) {
                return;
            }

            this.$targetInput = this.$el.closest(
                '.worth-facilitator-sign-in-participant'
            ).find('form select[name="participant_id"]');

            // Make an array containing a jQuery object for each
            // cohort ID.
            this.$options = this.$targetInput.find('option');

            // $allOptions is a read-only array of option elements
            // that always contains all the options.
            this.$allOptions = this.$options.clone(true);

            var filterVal = this.$el.val();
            this._updateDisplayedParticipants(filterVal);
        },

        change: function() {
            // The filter dropdown's value
            var filterVal = this.$el.val();
            this._updateDisplayedParticipants(filterVal);

            // Select the "Choose a Participant" setting
            this.$targetInput.find('>option:eq(0)').prop('selected', true);
        }
    });

    return SignInParticipantView;
});
