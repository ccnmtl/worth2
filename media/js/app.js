define([
    'jquery',
    'underscore',
    'backbone',
    'views/create-participant',
    'views/edit-participant',
    'views/sign-in-participant',
    'bootstrap',
    'jquery-cookie'
], function(
    $, _, Backbone,
    CreateParticipantView, EditParticipantView, SignInParticipantView
) {
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
        new CreateParticipantView();
        $('form.worth-edit-participant').each(function() {
            new EditParticipantView({
                el: $(this)
            });
        });

        new SignInParticipantView();
    };

    return {
        initialize: initialize
    };
});
