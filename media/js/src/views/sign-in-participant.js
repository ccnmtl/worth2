define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    var SignInParticipantView = Backbone.View.extend({
        el: '.worth-facilitator-sign-in-participant form',

        initialize: function() {
            this._refreshDisabledState(
                this.$el.find('.worth-participant-destination input:checked'));
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
            var $form = $target.closest('form');
            var $selectedOption = $target.find('option:selected');
            var lastLocation = $selectedOption.data('last-location');
            var nextLocation = $selectedOption.data('next-location');
            var highestAccessedSession = parseInt(
                $selectedOption.data('highest-accessed'), 10);

            $form.find('.worth-participant-last-location').text(lastLocation);
            $form.find('.worth-participant-next-location').text(nextLocation);

            // Enable the "Already completed" radio button if the
            // currently selected participant has completed any
            // sessions.
            var $alreadyCompletedRadioButton = $form.find(
                '.radio input[value="already_completed_session"]');
            if (highestAccessedSession > 1) {
                this._enableAlreadyCompletedRadioButton(
                    $alreadyCompletedRadioButton);
            } else {
                this._disableAlreadyCompletedRadioButton(
                    $alreadyCompletedRadioButton);
            }

            var $alreadyCompletedDropdown = $form.find(
                '#id_already_completed_session');

            // Store the checked option before re-populating it
            // with the selected participant's specific destinations.
            var savedVal = $alreadyCompletedDropdown.val();

            $alreadyCompletedDropdown.html('');
            var i;
            for (i = 1; i < highestAccessedSession; i++) {
                $alreadyCompletedDropdown.append(
                    '<option value="' + i + '">' +
                        'Session ' + i +
                        '</option>');
            }

            if (savedVal >= 1) {
                $alreadyCompletedDropdown.val(savedVal);
            }

            // Disable the "last completed activity" radio button if
            // selected participant is new, and has "None" as their
            // last location.
            var $input = $form.find(
                'input[value="last_completed_activity"]');
            var lastLocationText = $.trim(
                $form.find('.worth-participant-last-location').text());
            if (lastLocationText.toLowerCase() === 'none') {
                // disable
                this._disableLastCompletedRadioButton($input);
            } else {
                // enable
                this._enableLastCompletedRadioButton($input);
            }
        },

        /**
         * @param {jQuery element} $el - The button's <input> el.
         */
        _disableAlreadyCompletedRadioButton: function($el) {
            $el.prop({
                'checked': false,
                'disabled': true
            });
            $el.closest('.radio').addClass('disabled');
        },

        /**
         * @param {jQuery element} $el - The button's <input> el.
         */
        _enableAlreadyCompletedRadioButton: function($el) {
            $el.prop('disabled', false);
            $el.closest('.radio').removeClass('disabled');
        },

        /**
         * Disable the "already completed" dropdown.
         *
         * @param {jQuery element} $el - The <select> element.
         */
        _disableAlreadyCompletedDropdown: function($el) {
            $el.prop('disabled', true);
        },

        /**
         * Enable the "already completed" dropdown.
         *
         * @param {jQuery element} $el - The <select> element.
         */
        _enableAlreadyCompletedDropdown: function($el) {
            $el.prop('disabled', false);
        },

        _disableLastCompletedRadioButton: function($el) {
            $el.prop({
                'checked': false,
                'disabled': true
            });
            $el.closest('.radio').addClass('disabled');
        },

        _enableLastCompletedRadioButton: function($el) {
            $el.prop('disabled', false);
            $el.closest('.radio').removeClass('disabled');
        },

        /**
         * Refresh the state of the "already completed" dropdown.
         */
        _refreshDisabledState: function($el) {
            var $select = $('#id_already_completed_session');
            if ($el.length === 0) {
                this._disableAlreadyCompletedDropdown($select);
                return;
            }
            // Only look at the radio buttons
            if ($el.prop('type') !== 'radio') {
                return;
            }
            var $parent = $el.closest('.worth-participant-destination');
            if ($parent.length > 0) {
                if ($el.prop('value') === 'already_completed_session') {
                    this._enableAlreadyCompletedDropdown($select);
                } else {
                    this._disableAlreadyCompletedDropdown($select);
                }
            }
        },

        /**
         * This event executes whenever the target changes:
         *   '.worth-facilitator-sign-in-participant form'
         */
        change: function(e) {
            var $target = $(e.target);
            this._refreshDisabledState($target);

            if ($target.attr('name') === 'participant_id') {
                this._updateParticipantDestinations($target);
            }
        }
    });

    return SignInParticipantView;
});
