define([
    'jquery',
    'views/goal-setting-form',
    'views/goal-checkin-form',
    'views/locked-video',
    'views/self-talk-road',
    'views/quiz-validator',
    'js-cookie'
], function(
    $,
    GoalSettingFormView, GoalCheckinFormView, LockedVideo, SelfTalkRoad,
    QuizValidator, Cookies
) {
    $(function() {
        var csrftoken = Cookies.get('csrftoken');
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
