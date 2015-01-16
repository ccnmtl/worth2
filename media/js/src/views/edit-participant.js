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
                study_id: this.$el.find('input[name=study_id]').val()
            });
            this.$el.find('button[name=is_archived]')
                .on('click', function(e) {
                    me.updateModel({
                        study_id: me.model.get('study_id'),
                        is_archived: true
                    }, $(e.target));
                });
        },
        submit: function(e) {
            this.id = this.$el.closest('.modal').data('id');
            e.preventDefault();
            var $target = $(e.currentTarget);
            var newStudyId = $target.find('input[name=study_id]').val();
            this.updateModel({study_id: newStudyId}, $target);
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

    return EditParticipantView;
});
