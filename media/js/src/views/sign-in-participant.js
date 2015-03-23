define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var SignInParticipantView = Backbone.View.extend({
        el: '.worth-facilitator-sign-in-participant form',
        initialize: function() {
            this.refreshDisabledState(
                this.$el.find('.worth-participant-destination input:checked'));
        },

        events: {
            change: 'change'
        },

        change: function(e) {
            var $target = $(e.target);
            this.refreshDisabledState($target);

            if ($target.attr('name') === 'participant_id') {
                var lastLocation = $target.find('option:selected')
                    .data('last-location');
                var nextLocation = $target.find('option:selected')
                    .data('next-location');

                $target.closest('form')
                    .find('.worth-participant-last-location')
                    .text(lastLocation);
                $target.closest('form')
                    .find('.worth-participant-next-location')
                    .text(nextLocation);
            }

        },

        refreshDisabledState: function($el) {
            var $parent = $el.closest('.worth-participant-destination');
            if ($parent.length > 0) {
                if ($el.prop('value') === 'already_completed_session') {
                    $parent.find('.worth-already-completed')
                        .prop('disabled', false);
                } else {
                    $parent.find('.worth-already-completed')
                        .prop('disabled', true);
                }
            }
        }
    });

    return SignInParticipantView;
});
