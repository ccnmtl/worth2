define([
    'jquery',
    'underscore',
    'backbone',
    'views/youtube-player',
], function($, _, Backbone, youtubePlayer) {
    /**
     * This is a backbone view used to initialize a locked YouTube video.
     */
    var LockedVideo = Backbone.View.extend({
        el: '#youtube-player',
        initialize: function() {
            if ($('#youtube-player').length === 0) {
                return;
            }

            youtubePlayer.loadYouTubeAPI(
                $('#youtube-player')[0], lockedVideoId);
        }
    });

    return LockedVideo;
});
