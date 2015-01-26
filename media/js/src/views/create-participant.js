define([
    'jquery',
    'underscore',
    'backbone',
    'models/participant'
], function($, _, Backbone, Participant) {
    var CreateParticipantView = Backbone.View.extend({
        el: '#worth-create-participant',
        events: {
            submit: 'submit'
        },
        submit: function(e) {
            e.preventDefault();
            var $target = $(e.currentTarget);
            var newStudyId = $target.find('input[name=study_id]').val();
            var person = new Participant({
                study_id: newStudyId
            });

            $.ajax({
                type: 'POST',
                url: '/api/participants/',
                data: {
                    study_id: newStudyId
                },
                success: function(data) {
                    $target.find('.worth-errors').hide();
                    $target.find('.worth-success').show();
                    location.reload();
                },
                error: function(xhr, status, error) {
                    var msg;
                    if (xhr.responseJSON &&
                        xhr.responseJSON.participant.studyId
                       ) {
                        msg = 'Error: Study ID: ' +
                            xhr.responseJSON.participant.studyId;
                    } else {
                        msg = error;
                    }
                    $target.find('.worth-success').hide();
                    $target.find('.worth-errors').show().text(msg);
                }
            });
        }
    });

    return CreateParticipantView;
});
