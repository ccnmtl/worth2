define([
    'jquery',
    'underscore',
    'backbone',
], function($, _, Backbone) {
    var SignInParticipantView = Backbone.View.extend({
        el: 'select#sign-in-cohort-filter',
        events: {
            change: 'change'
        },
        initialize: function() {
            if ($('.worth-facilitator-sign-in-participant').length !== 1) {
                return;
            }

            this.$targetInput = this.$el.closest(
                '.worth-facilitator-sign-in-participant'
            ).find('form select[name=participant_id]');

            // Make an array containing a jQuery object for each
            // cohort ID.
            this.$options = this.$targetInput.find('option');
        },
        change: function() {
            // The filter dropdown's value
            var filterVal = this.$el.val();

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

            // Select the "Choose a Participant" setting
            this.$targetInput.find('>option:eq(0)').prop('selected', true);
        }
    });

    return SignInParticipantView;
});
