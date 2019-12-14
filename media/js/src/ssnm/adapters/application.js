(function() {
    'use strict';
    var token = $('meta[name="csrf-token"]').attr('content');
    Ssnm.ApplicationAdapter = DS.JSONAPIAdapter.extend({
        namespace: 'ssnm/api',
        headers: {
            'X-CSRFToken': token
        }
    });
})();
