define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    /**
     * This view unlocks the page's "Next" button.
     */
    var Unlocker = Backbone.View.extend({
        unlock: function() {
            $('li.next').removeClass('disabled');
        },
        initialize: function() {
            if ($('#youtube-player').length === 0) {
                if (isSectionUnlocked === 1) {
                    this.unlock();
                }
            } else {
                // There's a video on the page, so find out if the user
                // has already watched it.
                var me = this;
                $.get('/api/watched_videos/', function(data) {
                    var match = _.find(data, function(e) {
                        return e.video_block === videoBlockId;
                    });
                    if (typeof match !== 'undefined') {
                        me.unlock();
                    }
                });
            }
        }
    });

    return Unlocker;
});
