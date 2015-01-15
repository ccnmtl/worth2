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
            var influenceDisplay = this.get('influenceDisplay');

            var str = '';
            if (influenceDisplay) {
                str = influenceDisplay;
            } else {
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
            }

            if (str) {
                str = str + ' Influence';
            }

            return str;
        }.property('influence', 'influenceDisplay')
    });
})();
