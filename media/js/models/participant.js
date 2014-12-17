define([
    'underscore',
    'backbone'
], function(_, Backbone) {
    var Participant = Backbone.Model.extend({
        urlRoot: '/api/participants',
        defaults: function() {
            return {
                study_id: '',
                is_archived: false
            };
        }
    });
    return Participant;
});
