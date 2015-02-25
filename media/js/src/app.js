define([
    'jquery',
    'underscore',
    'backbone',
    'views/create-participant',
    'views/edit-participant',
    'views/sign-in-participant',
    'views/manage-participant-filter',
    'views/sign-in-participant-filter',
    'views/goal-setting-form',
    'views/goal-checkin-form',
    'views/gated-video',
    'bootstrap',
    'jquery-cookie'
], function(
    $, _, Backbone,
    CreateParticipantView, EditParticipantView, SignInParticipantView,
    ManageParticipantFilter, SignInParticipantFilter, GoalSettingFormView,
    GoalCheckinFormView, GatedVideo
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

        new ManageParticipantFilter();

        new SignInParticipantFilter();

        new GoalSettingFormView();

        new GoalCheckinFormView();

        new GatedVideo();

        if ($('#youtube-player').length === 0) {
            $('li.next').removeClass('disabled');
        }
    };

    return {
        initialize: initialize
    };
});
