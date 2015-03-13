define([
    'jquery',
    'underscore',
    'backbone',
    'threejs',
    'tweenjs'
], function($, _, Backbone, THREE, TWEEN) {
    /**
     * A view for adding the self-talk road that displays an avatar in
     * different positions as the user selects form elements.
     */
    var SelfTalkRoad = Backbone.View.extend({
        // Position of the avatar on the road, on a scale of 0 to 1.
        position: 0,

        /**
         * @function draw
         *
         * Draw the scene with three.js and begin the render loop.
         */
        draw: function($container) {
            // .width() sometimes doesn't return an integer
            var w = $container.innerWidth();
            var h = $container.innerHeight();
            var scene = new THREE.Scene();
            var camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 1000);

            var renderer = new THREE.WebGLRenderer({
                alpha: true,
                antialias: true
            });

            // For retina compatibility
            renderer.setPixelRatio(
                window.devicePixelRatio ? window.devicePixelRatio : 1);
            renderer.setSize(w, h);

            $(renderer.domElement).addClass('embed-responsive-item');
            $container.append(renderer.domElement);

            // Draw road
            var road = new THREE.Mesh(
                new THREE.PlaneBufferGeometry(25, 1),
                new THREE.MeshLambertMaterial({
                    color: 0x002020
                })
            );
            road.position.x = -5;
            road.position.y = -0.5;
            road.rotation.x = -Math.PI / 2;

            scene.add(road);

            // Draw avatar
            var me = this;
            var map = THREE.ImageUtils.loadTexture(
                STATIC_URL + 'img/worth-selftalk-avatar.png', {}, function() {
                    var $form = $('.statement-form:first');
                    me.updatePosition($form);
                    renderer.render(scene, camera);
                });

            var material = new THREE.SpriteMaterial({
                map: map, color: 0xffffff, fog: true});
            this.sprite = new THREE.Sprite(material);

            scene.add(this.sprite);

            var light = new THREE.AmbientLight(0xf0e000);
            scene.add(light);

            camera.position.set(6, 1, 1);
            camera.lookAt(new THREE.Vector3(3, 0, 0));

            requestAnimationFrame(function render() {
                requestAnimationFrame(render);
                renderer.render(scene, camera);
                TWEEN.update();
            });
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

            if (this.sprite) {
                var target = {x: this.position * 4.5};
                var tween = new TWEEN.Tween(this.sprite.position).to(
                    target, 200);
                tween.start();
            }
        },

        initialize: function() {
            var $blocks = $(
                '#selftalk-statement-block,#selftalk-refutation-block');
            if ($blocks.length < 1) {
                return;
            }

            var me = this;
            var $container = $(
                '.worth-self-talk-road:first .embed-responsive');

            // Attach form events to this.position.
            var $form = $('.statement-form:first');

            var $inputs = $form.find('input[type=checkbox]');
            $inputs.each(function(k, v) {
                var $v = $(v);
                $v.on('change', function() {
                    me.updatePosition($form);
                });
            });

            this.draw($container);
        }
    });

    return SelfTalkRoad;
});
