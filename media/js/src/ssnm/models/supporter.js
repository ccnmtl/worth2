/*global Ssnm, DS */
(function() {
    'use strict';

    var attr = DS.attr;

    Ssnm.Supporter = DS.Model.extend({
        name: attr('string'),
        closeness: attr('string'),
        influence: attr('string'),
        influenceDisplay: attr('string'),
        providesEmotionalSupport: attr('boolean'),
        providesPracticalSupport: attr('boolean'),

        /**
         * Infer the human-readable influence from the influence attribute,
         * or from the influenceDisplay provided by the back-end if
         * possible. Returns a string.
         */
        displayInfluence: function() {
            var str = '';
            var influence = this.get('influence');

            if (influence === 'P') {
                str = 'Positive';
            } else if (influence === 'MP') {
                str = 'Mostly Positive';
            } else if (influence === 'MN') {
                str = 'Mostly Negative';
            } else if (influence === 'N') {
                str = 'Negative';
            }

            if (str === '') {
                // If, for some reason, the influence couldn't be read,
                // get the influenceDisplay from the back-end.
                str = this.get('influenceDisplay');
            }

            if (str) {
                str = str + ' Influence';
            }

            return str;
        }.property('influence', 'influenceDisplay'),

        influenceGlyphicon: function() {
            var influence = this.get('influence');
            if (influence === 'P' || influence === 'MP') {
                return '<span class="glyphicon glyphicon-plus" ' +
                    'aria-hidden="true"></span>';
            } else {
                return '<span class="glyphicon glyphicon-minus" ' +
                    'aria-hidden="true"></span>';
            }
        }.property('influence')
    });
})();
