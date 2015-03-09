define([
    'jquery',
    'underscore',
    'backbone',
], function($, _, Backbone) {
    /**
     * A view for adding the self-talk road that displays an avatar in
     * different positions as the user selects form elements.
     */
    var SelfTalkRoad = Backbone.View.extend({
        // Position of the avatar on the road, on a scale of 0 to 1.
        position: 0.9,

        /**
         * @function draw
         *
         * Draw the scene on the canvas.
         */
        draw: function(canvas) {
            var cw = canvas.width;
            var ch = canvas.height;
            var ctx = canvas.getContext('2d');

            ctx.clearRect(0, 0, cw, ch);

            // Make a yellow radial gradient for the road
            var gradient = ctx.createRadialGradient(
                cw * 0.75, ch * 0.75, 1,
                cw * 0.75, ch * 0.75, cw * 0.9);
            gradient.addColorStop(0, 'yellow');
            gradient.addColorStop(1, 'black');

            // Draw the road
            ctx.fillStyle = 'black';

            ctx.beginPath();
            ctx.moveTo(0, ch * 0.2);
            ctx.lineTo(cw * 0.75, ch);
            ctx.lineTo(cw, ch * 0.8);
            ctx.lineTo(0, ch * 0.2);
            ctx.lineWidth = 0.01;
            ctx.stroke();

            ctx.fillStyle = gradient;
            ctx.fill();

            // Draw the avatar
            var img = new Image();
            var me = this;
            img.onload = function() {
                var w = this.width;
                var h = this.height;

                var aspectRatio = h / w;

                var scaledWidth = (cw * me.position / 4) + 20;
                var scaledHeight = scaledWidth * aspectRatio;

                var scaledPos = me.position * 0.6;
                var scaledX = (scaledPos) * cw;

                // The y-pos is dependent on me.position as well as the
                // avatar's height
                var scaledY = Math.pow(scaledHeight, -2) + 60;

                ctx.drawImage(
                    img,
                    scaledX, scaledY,
                    scaledWidth, scaledHeight);
            };
            // TODO: this url should point to django's STATIC_URL
            img.src = '/media/img/worth-selftalk-avatar.png';
        },

        /**
         * @function updateCanvasDimensions
         *
         * Updates the canvas's width and height based on its container's
         * dimensions.
         */
        updateCanvasDimensions: function(canvas) {
            var $container = $(canvas).closest('.worth-self-talk-road');

            // Double the canvas's width and height attributes for
            // retina screens.
            //canvas.style.width = $container.innerWidth() + 'px';
            //canvas.style.height = $container.innerHeight() + 'px';
            canvas.width = $container.innerWidth() * 2;
            canvas.height = $container.innerHeight() * 2;
        },

        /**
         * @function updatePosition
         *
         * This function looks at each input's value in the container
         * and updates this.position based on how many are checked off
         * (for external self-talk), or filled in (for internal self-talk).
         */
        updatePosition: function($container) {
            var total = $container.find('input:checkbox').length;
            var checked = $container.find('input:checkbox:checked').length;
            var ratio = checked / total;
            this.position = 1 - ratio;
        },

        initialize: function() {
            var $blocks = $('.worth-statement-block,.worth-refutation-block');
            if ($blocks.length < 1) {
                return;
            }

            var me = this;
            var canvas = document.getElementById('selftalk-road-canvas');

            // Note that resizing will never occur on the iPad, but it's
            // useful to have in here for desktop.
            $(window).on('resize', function() {
                me.updateCanvasDimensions(canvas);
                me.draw(canvas);
            });

            // Attach form events to this.position.
            var $form = $('.statement-form:first');

            var $inputs = $form.find('input[type=checkbox]');
            $inputs.each(function(k, v) {
                var $v = $(v);
                $v.on('change', function() {
                    me.updatePosition($form);
                    me.draw(canvas);
                });
            });

            this.updatePosition($form);
            this.updateCanvasDimensions(canvas);
            this.draw(canvas);
        }
    });

    return SelfTalkRoad;
});
