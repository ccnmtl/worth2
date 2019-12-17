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
        underscore: '../lib/underscore',
        backbone: '../lib/backbone',
        threejs: '../lib/three.min',
        tweenjs: '../lib/Tween'
    },
    urlArgs: 'bust=' + (new Date()).getTime()
});

require([
    'app'
], function(App) {
    App.initialize();
});
