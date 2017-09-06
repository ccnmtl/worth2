define([
    'jquery',
    'underscore',
    'backbone',
    'models/participant',
    'utils'
], function($, _, Backbone, Participant, utils) {
    var CreateParticipantView = Backbone.View.extend({
        el: '#worth-create-participant',
        events: {
            submit: 'submit'
        },
        submit: function(e) {
            e.preventDefault();
            var $target = $(e.currentTarget);
            var newStudyId = $target.find('input[name="study_id"]').val();

            new Participant({
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
                    if (xhr.responseJSON) {
                        msg = utils.formatDrfJsonErrorsToHtml(xhr.responseJSON);
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
