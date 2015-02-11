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
                    var msg = '';

                    // Find validation errors in participant response object
                    if (xhr.responseJSON && xhr.responseJSON.participant) {
                        for (var key in xhr.responseJSON.participant) {
                            msg += '<div>' +
                                xhr.responseJSON.participant[key] +
                                '</div>';
                        }
                    } else {
                        msg = error;
                    }
                    $target.find('.worth-success').hide();
                    $target.find('.worth-errors').show().html(msg);
                }
            });
        }
    });

    return CreateParticipantView;
});
