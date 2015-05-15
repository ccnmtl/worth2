define([
    'jquery',
    'models/watched-video',
    'utils'
], function($, WatchedVideo, utils) {
    var youtubePlayer = {
        loadYouTubeAPI: function(container, videoId) {
            if (typeof YT === 'undefined' ||
                typeof YT.Player === 'undefined'
               ) {
                window.onYouTubeIframeAPIReady = function() {
                    youtubePlayer.loadPlayer(container, videoId);
                };

                $.getScript('//www.youtube.com/iframe_api');
            } else {
                youtubePlayer.loadPlayer(container, videoId);
            }
        },

        loadPlayer: function(container, videoId) {
            new YT.Player(container, {
                videoId: videoId,
                width: 640,
                height: 390,
                playerVars: {
                    'autoplay': 1,
                    'controls': 1,
                    'modestbranding': 1,
                    'rel': 0,
                    'showinfo': 0
                },
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });
        }
    };

    /**
     * Save a WatchedVideo to the server.
     */
    function recordWatchedVideo(videoId) {
        var watchedVideo = new WatchedVideo({'video_id': videoId});
        watchedVideo.save(null, {
            success: function() {
                $('li.next').removeClass('disabled');
            }
        });
    }

    /**
     * This YouTube IFrame API calls this global function when the
     * video's state changes.
     */
    window.onPlayerStateChange = function(event) {
        if (event.data === YT.PlayerState.ENDED) {
            // The video ended, so unlock the 'next' button.
            recordWatchedVideo(lockedVideoId);
        }
    };

    window.onPlayerReady = function(event) {
        var player = event.target;
        var seconds = player.getDuration();
        var videoDuration = utils.secondsToHms(seconds);
        if (videoDuration.length > 0) {
            $('#worth-youtube-video-duration').html(
                'Video Duration: <time>' + videoDuration + '</time>');
        }
    };

    return youtubePlayer;
});
