define([
    'jquery',
    'models/watched-video'
], function($, WatchedVideo) {
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
                    autoplay: 1,
                    controls: 0,
                    modestbranding: 1,
                    rel: 0,
                    showinfo: 0
                },
                events: {
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

    return youtubePlayer;
});
