require.config({
    shim: {
        bootstrap: { deps: ['jquery'] }
    },
    paths: {
        jquery: './lib/jquery',
        'jquery-cookie': './lib/jquery.cookie',
        underscore: './lib/underscore',
        backbone: './lib/backbone',
        bootstrap: '//netdna.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min'
    }
});

require([
    'app'
], function(App) {
    App.initialize();
});
