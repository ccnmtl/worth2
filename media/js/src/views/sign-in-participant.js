define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var SignInParticipantView = Backbone.View.extend({
        el: '.worth-facilitator-sign-in-participant form',

        initialize: function() {
            var $target = this.$el.find('#id_participant_id');
            var $participant = $target.find('option:checked');
            this._updateParticipantDestinations($target, $participant);
        },

        events: {
            change: 'change'
        },

        /**
         * This function updates the text for participants' destinations
         * on the participant sign-in form.
         */
        _updateParticipantDestinations: function($target, $participant) {
            $('.completed-percentage').remove();
            if (typeof $participant.attr('value') === 'undefined') {
                return;
            }

            var $form = $target.closest('form');

            for (var i = 0; i < 5; i++) {
                var $el = $form.find('#id_participant_destination_' + i);
                var $label = $el.closest('label');
                var percentCompleted = $participant.data(
                    'module-' + 'abcde'[i] + '-complete');

                $label.append(
                    '<span class="completed-percentage">' +
                        percentCompleted +
                        '% complete</span>');
            }
        },

        _updateParticipantSignedInAlert: function($target, $participant) {
            var isLoggedIn = $participant.data('is-recently-logged-in');
            if (isLoggedIn === 'True') {
                $('.participant-signin-warning').show();
            } else {
                $('.participant-signin-warning').hide();
            }
        },

        /**
         * This event executes whenever the target changes:
         *   '.worth-facilitator-sign-in-participant form'
         */
        change: function(e) {
            var $target = $(e.target);

            if ($target.attr('name') === 'participant_id') {
                var $participant = $target.find('option:checked');
                this._updateParticipantDestinations($target, $participant);
                this._updateParticipantSignedInAlert($target, $participant);
            }
        }
    });

    return SignInParticipantView;
});
