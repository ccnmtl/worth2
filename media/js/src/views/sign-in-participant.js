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
        },

        events: {
            change: 'change'
        },

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
                '.worth-already-completed');
            $alreadyCompletedDropdown.html('');
            var i;
            for (i = 1; i < highestAccessedSession; i++) {
                $alreadyCompletedDropdown.append(
                    '<option value="' + i + '">' +
                        'Session ' + i +
                        '</option>');
            }
        },

        /**
         * @param {jQuery element} $el - The button's <input> el.
         */
        _disableAlreadyCompletedRadioButton: function($el) {
            $el.prop('disabled', true);
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

        _refreshDisabledState: function($el) {
            var $parent = $el.closest('.worth-participant-destination');
            if ($parent.length > 0) {
                var $select = $parent.find('select.worth-already-completed');
                if ($el.prop('value') === 'already_completed_session') {
                    this._enableAlreadyCompletedDropdown($select);
                } else {
                    this._disableAlreadyCompletedDropdown($select);
                }
            }
        },

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
