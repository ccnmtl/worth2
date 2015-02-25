define([
    'jquery',
    'underscore',
    'backbone',
    'views/youtube-player',
], function($, _, Backbone, youtubePlayer) {
    var GatedVideo = Backbone.View.extend({
        el: '#youtube-player',
        initialize: function() {
            if ($('#youtube-player').length === 0) {
                return;
            }

            youtubePlayer.loadYouTubeAPI(
                $('#youtube-player')[0], gatedVideoId);
        }
    });

    return GatedVideo;
});
