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
            this.refreshDisabledState($(e.target));
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
