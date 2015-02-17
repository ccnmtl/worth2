define([
    'jquery',
    'underscore',
    'backbone',
], function($, _, Backbone) {
    var ManageParticipantView = Backbone.View.extend({
        el: 'select#manage-cohort-filter',

        events: {
            change: 'change'
        },

        initialize: function() {
            if ($('.worth-facilitator-manage-participants').length !== 1) {
                return;
            }

            // Make an array containing a jQuery object for each
            // cohort ID.
            this.$childEls = this.$el.closest(
                '.worth-facilitator-manage-participants'
            ).find('.worth-cohort-container .worth-cohort-id');
        },

        change: function() {
            // The filter dropdown's value
            var filterVal = this.$el.val();

            this.$childEls.each(function(k, v) {
                var $v = $(v);
                var val = $.trim($v.text());
                if ('all' === filterVal || val === filterVal) {
                    $v.closest('.row').show();
                } else {
                    $v.closest('.row').hide();
                }
            });
        }
    });

    return ManageParticipantView;
});
