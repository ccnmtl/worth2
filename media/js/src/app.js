define([
    'jquery',
    'views/goal-setting-form',
    'views/goal-checkin-form',
    'views/locked-video',
    'views/self-talk-road',
    'views/quiz-validator'
], function(
    $,
    GoalSettingFormView, GoalCheckinFormView, LockedVideo, SelfTalkRoad,
    QuizValidator
) {
    $(function() {
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    var token = $('meta[name="csrf-token"]').attr('content');
                    xhr.setRequestHeader('X-CSRFToken', token);
                }
            }
        });
    });
    var initialize = function() {
        new GoalSettingFormView();

        new GoalCheckinFormView();

        new LockedVideo();

        new SelfTalkRoad();

        new QuizValidator();
    };

    return {
        initialize: initialize
    };
});
