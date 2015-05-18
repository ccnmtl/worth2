define([
    'jquery',
    'underscore',
    'backbone',
    'models/participant'
], function($, _, Backbone, Participant) {
    var EditParticipantView = Backbone.View.extend({
        el: 'form.worth-edit-participant',
        events: {
            submit: 'submit'
        },
        initialize: function() {
            var me = this;
            this.id = this.$el.closest('.modal').data('id');
            this.model = new Participant({
                id: this.id,
                study_id: this.$el.find('input[name="study_id"]').val(),
                cohort_id: this.$el.find('input[name="cohort_id"]').val()
            });
        },
        submit: function(e) {
            this.id = this.$el.closest('.modal').data('id');
            e.preventDefault();
            var $target = $(e.currentTarget);
            var newStudyId = $target.find('input[name="study_id"]').val();
            var newCohortId = $target.find('input[name="cohort_id"]').val();
            this.updateModel({
                study_id: newStudyId,
                cohort_id: newCohortId
            }, $target);
        },
        updateModel: function(data, $target) {
            $.ajax({
                type: 'PUT',
                url: this.model.url(),
                data: data,
                success: function(data) {
                    $target.find('.worth-errors').hide();
                    $target.find('.worth-success').show();
                    location.reload();
                },
                error: function(xhr, status, error) {
                    var msg = '';

                    // Find validation errors in participant response object
                    if (xhr.responseJSON) {
                        for (var key in xhr.responseJSON) {
                            msg += '<div>' + xhr.responseJSON[key] + '</div>';
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

    return EditParticipantView;
});
