/*global Ssnm, DS */
(function() {
    'use strict';

    Ssnm.Supporter = DS.Model.extend({
        name: DS.attr('string'),
        closeness: DS.attr('string'),
        influence: DS.attr('string'),
        getInfluenceDisplay: DS.attr('string'),
        providesEmotionalSupport: DS.attr('boolean'),
        providesPracticalSupport: DS.attr('boolean')
    });
})();
