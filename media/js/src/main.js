require.config({
    shim: {
        bootstrap: {
            deps: ['jquery']
        },
        jquery: {
            exports: '$'
        },
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        },
        threejs: {
            exports: 'THREE'
        },
        tweenjs: {
            exports: 'TWEEN'
        }
    },
    paths: {
        jquery: '../lib/jquery',
        'js-cookie': '../lib/js.cookie',
        underscore: '../lib/underscore',
        backbone: '../lib/backbone',
        threejs: '../lib/three.min',
        tweenjs: '../lib/tween.min'
    },
    urlArgs: 'bust=' + (new Date()).getTime()
});

require([
    'app'
], function(App) {
    App.initialize();
});
