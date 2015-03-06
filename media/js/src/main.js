require.config({
    shim: {
        bootstrap: {
            deps: ['jquery']
        },
        'jquery-cookie': {
            deps: ['jquery']
        },
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        }
    },
    paths: {
        jquery: '../lib/jquery',
        'jquery-cookie': '../lib/jquery.cookie',
        underscore: '../lib/underscore',
        backbone: '../lib/backbone'
    },
    urlArgs: 'bust=' + (new Date()).getTime()
});

require([
    'app'
], function(App) {
    App.initialize();
});
