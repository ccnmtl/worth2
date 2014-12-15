$(function() {
    var Participant = Backbone.Model.extend({
        defaults: function() {
            return {
                study_id: '',
                is_archived: false
            };
        }
    });

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
                    if (xhr.responseJSON && xhr.responseJSON.study_id) {
                        msg = 'Error: Study ID: ' + xhr.responseJSON.study_id;
                    } else {
                        msg = error;
                    }
                    $target.find('.worth-success').hide();
                    $target.find('.worth-errors').show().text(msg);
                }
            });
        }
    });

    var App = new CreateParticipantView();
});
