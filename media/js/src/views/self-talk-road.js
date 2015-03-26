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

        addLighting: function(scene) {
            var directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(0, 1, 0.5);
            scene.add(directionalLight);

            var lights = [];
            lights[0] = new THREE.PointLight(0xffffff, 1, 2.3);
            lights[1] = new THREE.PointLight(0xffffff, 1, 2.3);
            lights[2] = new THREE.PointLight(0xffffff, 1, 2.3);

            lights[0].position.set(6, 1, 0);
            lights[1].position.set(6, 1, 1);
            lights[2].position.set(6, 1, -1);

            scene.add(lights[0]);
            scene.add(lights[1]);
            scene.add(lights[2]);
        },

        addObjects: function(scene, renderer, camera) {
            // Draw ground
            var groundGeometry = new THREE.PlaneBufferGeometry(44, 100, 0);
            var ground = new THREE.Mesh(
                groundGeometry,
                new THREE.MeshLambertMaterial({
                    color: 0xd092f0
                })
            );
            ground.position.x = -15;
            ground.position.y = -0.61;
            ground.rotation.x = -Math.PI / 2;

            scene.add(ground);

            // Draw road
            var roadGeometry = new THREE.BoxGeometry(44, 1, 0.1);
            var road = new THREE.Mesh(
                roadGeometry,
                new THREE.MeshLambertMaterial({
                    color: 0xfff010
                })
            );
            road.position.x = -15;
            road.position.y = -0.6;
            road.rotation.x = -Math.PI / 2;

            scene.add(road);

            // Draw avatar
            var me = this;
            var map = THREE.ImageUtils.loadTexture(
                STATIC_URL + 'img/selftalk-avatar.png', {}, function() {
                    renderer.render(scene, camera);
                });

            var material = new THREE.SpriteMaterial({
                map: map, color: 0xffffff, fog: true});
            this.sprite = new THREE.Sprite(material);
            this.sprite.position.x = this.position * 4.5;

            scene.add(this.sprite);
        },

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

            this.addObjects(scene, renderer, camera);
            this.addLighting(scene);

            camera.position.set(6, 0.6, 1);
            camera.lookAt(new THREE.Vector3(3, -0.5, 0));

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
         * Calculate position based on the checkbox form.
         *
         * 'type' is either "refutation" or "statement".
         *
         * Returns a number.
         */
        calcPosForCheckboxForm: function($form, type) {
            var total = $form.find('input:checkbox').length;
            var checked = $form.find('input:checkbox:checked').length;
            var ratio = checked / total;

            var newPos;
            if (type === 'statement') {
                newPos = ratio;
            } else {
                newPos = 1 - ratio;
            }

            return newPos;
        },

        /**
         * Look at each checkbox in the form and set up a
         * listener to update this.position.
         *
         * 'type' is either "refutation" or "statement".
         */
        initForCheckboxForm: function($form, type) {
            var $inputs = $form.find('input:checkbox');
            var me = this;

            $inputs.each(function(k, v) {
                var $v = $(v);
                $v.on('change', function() {
                    var newPos = me.calcPosForCheckboxForm($form, type);
                    me.updatePosition(newPos);
                });
            });

            this.updatePosition(
                this.calcPosForCheckboxForm($form, type));
        },

        /**
         * Calculate position based on the dropdown form.
         *
         * 'type' is either "refutation" or "statement".
         *
         * Returns a number.
         */
        calcPosForDropdownForm: function($form, type) {
            var $selects = $form.find('select');
            var total = $selects.length;
            var selected = _.filter(
                $selects,
                function(el) {
                    return $(el).val() > 0;
                }
            ).length;
            var ratio = selected / total;

            var newPos;
            if (type === 'statement') {
                newPos = 1 - ratio;
            } else {
                newPos = ratio;
            }

            return newPos;
        },

        /**
         * Look at each dropdown in the form and set up a
         * listener to update this.position.
         *
         * 'type' is either "refutation" or "statement".
         */
        initForDropdownForm: function($form, type) {
            var $selects = $form.find('select');
            var me = this;

            $selects.each(function(k, v) {
                var $v = $(v);
                $v.on('change', function() {
                    var newPos = me.calcPosForDropdownForm($form, type);
                    me.updatePosition(newPos);
                });
            });

            this.updatePosition(
                this.calcPosForDropdownForm($form, type));
        },

        initialize: function() {
            var $blocks = $(
                '#selftalk-statement-block,#selftalk-refutation-block');
            if ($blocks.length < 1) {
                return;
            }

            // Attach form events to this.position.
            var $refutationForm = $('.refutation-form:first');
            var $statementForm = $('.statement-form:first');
            if ($refutationForm.find('select').length > 0) {
                this.initForDropdownForm($refutationForm, 'refutation');
            } else if ($statementForm.find('select').length > 0) {
                this.initForDropdownForm($statementForm, 'statement');
            } else if ($refutationForm.find('input:checkbox').length > 0) {
                this.initForCheckboxForm($refutationForm);
            } else if ($statementForm.find('input:checkbox').length > 0) {
                this.initForCheckboxForm($statementForm);
            }

            var $container = $(
                '.worth-self-talk-road:first .embed-responsive');
            this.draw($container);
        }
    });

    return SelfTalkRoad;
});
