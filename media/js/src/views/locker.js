define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    /**
     * This view locks the page's "Next" button.
     *
     * It also displays a message when the user clicks on the
     * "Next" button when it's locked.
     */
    var Locker = Backbone.View.extend({
        lock: function() {
            $('li.next').addClass('disabled');
        },
        initialize: function() {
            if (typeof isSectionUnlocked !== 'undefined' &&
                isSectionUnlocked === 0
               ) {
                this.lock();
            }

            if ($('#youtube-player').length > 0) {
                // There's a video on the page, so find out if the user
                // has already watched it.
                var me = this;
                $.get('/api/watched_videos/', function(data) {
                    var match = _.find(data, function(e) {
                        return e.video_id === lockedVideoId;
                    });
                    if (typeof match === 'undefined') {
                        me.lock();
                    }
                });
            }

            $('.next').on('click', function(e) {
                if ($(this).hasClass('disabled')) {
                    e.preventDefault();
                    window.alert(
                        'Please finish everything on this screen ' +
                            'before moving forward.');
                }
            });
        }
    });

    return Locker;
});
