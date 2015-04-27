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
            this.$options.each(function(k, v) {
                var $v = $(v);

                // Ignore the "Choose a Participant" option
                if ($v.index() === 0) {
                    return;
                }

                var cohortId = String($v.data('cohort-id'));
                if ('all' === filterVal || cohortId === filterVal) {
                    $v.show();
                } else {
                    $v.hide();
                }
            });
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
