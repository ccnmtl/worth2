define([
    'underscore',
    'backbone'
], function(_, Backbone) {
    var WatchedVideo = Backbone.Model.extend({
        urlRoot: '/api/watched_videos/',
        defaults: function() {
            return {
                video_id: null
            };
        }
    });
    return WatchedVideo;
});
