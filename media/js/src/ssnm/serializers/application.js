(function() {
    Ssnm.ApplicationSerializer = DS.JSONAPISerializer.extend({
        keyForAttribute: function(attr) {
            return Em.String.underscore(attr);
        }
    });
})();
