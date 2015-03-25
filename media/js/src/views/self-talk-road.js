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
            var roadGeometry = new THREE.BoxGeometry(25, 1, 0.1);
            var road = new THREE.Mesh(
                roadGeometry,
                new THREE.MeshLambertMaterial({
                    color: 0xfff010
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
                    renderer.render(scene, camera);
                });

            var material = new THREE.SpriteMaterial({
                map: map, color: 0xffffff, fog: true});
            this.sprite = new THREE.Sprite(material);
            this.sprite.position.x = this.position * 4.5;

            scene.add(this.sprite);

            // Lighting
            var light = new THREE.AmbientLight(0xf0e000);
            scene.add(light);

            var lights = [];
            lights[0] = new THREE.PointLight(0xffffff, 1, 0);
            lights[1] = new THREE.PointLight(0xffffff, 1, 0);
            lights[2] = new THREE.PointLight(0xffffff, 1, 0);

            lights[0].position.set(0, 0, 0);
            lights[1].position.set(1, 0, 1);
            lights[2].position.set(-1, 0, -1);

            scene.add(lights[0]);
            scene.add(lights[1]);
            scene.add(lights[2]);

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
         * This function updates the three.js scene based on the input
         * position.
         */
        updatePosition: function(pos) {
            this.position = pos;

            if (this.sprite) {
                var target = {x: this.position * 4.5};
                var tween = new TWEEN.Tween(this.sprite.position).to(
                    target, 200);
                tween.start();
            }
        },

        /**
         * Calculate position based on the statement form.
         *
         * Returns a number.
         */
        calcPosForStatementForm: function($form) {
            var total = $form.find('input:checkbox').length;
            var checked = $form.find('input:checkbox:checked').length;
            var ratio = checked / total;
            var newPos = 1 - ratio;
            return newPos;
        },

        /**
         * Look at each checkbox in the statement form and set up a
         * listener to update this.position.
         */
        initForStatementForm: function($form) {
            var $inputs = $form.find('input:checkbox');
            var me = this;

            $inputs.each(function(k, v) {
                var $v = $(v);
                $v.on('change', function() {
                    var newPos = me.calcPosForStatementForm($form);
                    me.updatePosition(newPos);
                });
            });

            this.updatePosition(
                this.calcPosForStatementForm($form));
        },

        /**
         * Calculate position based on the refutation form.
         *
         * Returns a number.
         */
        calcPosForRefutationForm: function($form) {
            var $selects = $form.find('select');
            var total = $selects.length;
            var selected = _.filter(
                $selects,
                function(el) {
                    return $(el).val() > 0;
                }).length;
            var ratio = selected / total;
            var newPos = ratio;
            return newPos;
        },

        /**
         * Look at each dropdown in the refutation form and set up a
         * listener to update this.position.
         */
        initForRefutationForm: function($form) {
            var $selects = $form.find('select');
            var me = this;

            $selects.each(function(k, v) {
                var $v = $(v);
                $v.on('change', function() {
                    var newPos = me.calcPosForRefutationForm($form);
                    me.updatePosition(newPos);
                });
            });

            this.updatePosition(
                this.calcPosForRefutationForm($form));
        },

        initialize: function() {
            var $blocks = $(
                '#selftalk-statement-block,#selftalk-refutation-block');
            if ($blocks.length < 1) {
                return;
            }

            // Attach form events to this.position.
            if ($('#selftalk-statement-block').length === 1) {
                this.initForStatementForm(
                    $blocks.find('.statement-form:first'));
            } else if ($('#selftalk-refutation-block').length === 1) {
                this.initForRefutationForm(
                    $blocks.find('.refutation-form:first'));
            }

            var $container = $(
                '.worth-self-talk-road:first .embed-responsive');
            this.draw($container);
        }
    });

    return SelfTalkRoad;
});
