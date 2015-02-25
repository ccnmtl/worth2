define([
    'jquery',
], function($) {
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
                    autoplay: 0,
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

    window.onPlayerStateChange = function(event) {
        if (event.data === YT.PlayerState.ENDED) {
            // The video ended, so unlock the 'next' button.
            $('li.next').removeClass('disabled');
        }
    };

    return youtubePlayer;
});
