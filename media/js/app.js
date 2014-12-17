define([
    'jquery',
    'underscore',
    'backbone',
    'views/create-participant',
    'views/edit-participant',
    'bootstrap',
    'jquery-cookie'
], function($, _, Backbone, CreateParticipantView, EditParticipantView) {
    $(function() {
        var csrftoken = $.cookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    });
    var initialize = function() {
        var createParticipantView = new CreateParticipantView();
        $('form.worth-edit-participant').each(function() {
            new EditParticipantView({
                el: $(this)
            });
        });
    };

    return {
        initialize: initialize
    }
});
