define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var SignInParticipantView = Backbone.View.extend({
        el: '.worth-facilitator-sign-in-participant form',

        initialize: function() {
            this._updateParticipantDestinations(
                this.$el.find('#id_participant_id'));
        },

        events: {
            change: 'change'
        },

        /**
         * This function updates the text for participants' destinations
         * on the participant sign-in form.
         */
        _updateParticipantDestinations: function($target) {
            $('.completed-percentage').remove();

            var $participant = $target.find('option:checked');
            if (typeof $participant.attr('value') === 'undefined') {
                return;
            }

            var $form = $target.closest('form');
            var $destinations = $form.find(
                '#id_participant_destination>.radio input');
            var i;
            for (i = 0; i < 5; i++) {
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

        /**
         * This event executes whenever the target changes:
         *   '.worth-facilitator-sign-in-participant form'
         */
        change: function(e) {
            var $target = $(e.target);

            if ($target.attr('name') === 'participant_id') {
                this._updateParticipantDestinations($target);
            }
        }
    });

    return SignInParticipantView;
});
