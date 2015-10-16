define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    /**
     * This view unlocks the page's "Next" button.
     *
     * It also displays a message when the user clicks on the
     * "Next" button when it's locked.
     */
    var Unlocker = Backbone.View.extend({
        unlock: function() {
            $('li.next').removeClass('disabled');
        },
        initialize: function() {
            if (typeof isSectionUnlocked === 'undefined') {
                return;
            }

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
                        return e.video_id === lockedVideoId;
                    });
                    if (typeof match !== 'undefined') {
                        me.unlock();
                    }
                });
            }

            $('.next.disabled').on('click', function(e) {
                // Even though this event is bound only to disabled buttons,
                // we need to check to make sure the element still has the
                // disabled class, in case it's been changed.
                if ($(this).hasClass('disabled')) {
                    e.preventDefault();
                    window.alert(
                        'Please finish everything on this screen ' +
                            'before moving forward.');
                }
            });
        }
    });

    return Unlocker;
});
