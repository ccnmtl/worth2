define([
    'jquery',
    'underscore',
    'backbone',
], function($, _, Backbone) {
    /**
     * A view for adding avatar on the self-talk road that changes
     * as the user selects form elements.
     */
    var SelfTalkRoad = Backbone.View.extend({
        updateCanvasDimensions: function() {
            var $container = $('.worth-self-talk-road:first');
            var $canvas = $(this.canvas);
            $canvas.attr('width', $container.width());
            $canvas.attr('height', $container.height());
        },
        initialize: function() {
            var $blocks = $('.worth-statement-block,.worth-refutation-block');
            if ($blocks.length < 1) {
                return;
            }

            this.canvas = document.getElementById('selftalk-road-canvas');
            this.updateCanvasDimensions();
            var ctx = this.canvas.getContext('2d');

            ctx.fillStyle = 'black';

            ctx.beginPath();

            // Make a yellow radial gradient for the road
            var gradient = ctx.createRadialGradient(
                175, 75, 0, 175, 75, 200);
            gradient.addColorStop(0, 'yellow');
            gradient.addColorStop(1, 'black');

            // Draw the road
            ctx.moveTo(0, 0);
            ctx.lineTo(200, 200);
            ctx.lineTo(300, 180);
            ctx.lineTo(0, 0);
            ctx.lineWidth = 0.01;
            ctx.stroke();
            ctx.fillStyle = gradient;
            ctx.fill();

            var img = new Image();
            img.onload = function() {
                ctx.drawImage(img, 180, 0, 40, 180);
            };
            img.src = '/media/img/worth-selftalk-avatar.png';

            $(window).resize(this.updateCanvasDimensions);
        }
    });

    return SelfTalkRoad;
});
