define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    /**
     * This view adds quiz validation to all the quizzes in Worth 2.
     */
    var QuizValidator = Backbone.View.extend({
        /**
         * This function returns false if all the radio buttons on the
         * form are unchecked. Otherwise, it returns true.
         */
        validateRadioButtons: function($form) {
            var $radioButtons = $form.find('input[type="radio"]');
            var hasAnyCheckedRadioButtons = _.reduce(
                $radioButtons,
                function(memo, $el) {
                    return memo || $($el).is(':checked');
                },
                false);

            if ($radioButtons.length > 0 && !hasAnyCheckedRadioButtons) {
                return false;
            }

            return true;
        },

        /**
         * This function returns false if any of the text inputs in the
         * questions containing `cssClass` are not filled in. cssClass
         * defaults to 'quizblock-required'.
         */
        validateRequiredInputs: function($form, cssClass) {
            if (typeof cssClass === 'undefined') {
                cssClass = 'quizblock-required';
            }

            var $requiredQuestionInputs = $form
                .find('.casequestion.' + cssClass)
                .find('input[type="text"],textarea');

            var hasAnyBlankTextInputs = _.reduce(
                $requiredQuestionInputs,
                function(memo, $el) {
                    var isBlank = $.trim($($el).val()).length === 0;
                    return memo || isBlank;
                },
                false);

            if ($requiredQuestionInputs.length > 0 &&
                hasAnyBlankTextInputs
               ) {
                return false;
            }

            return true;
        },

        initialize: function() {
            // Don't use this JS validator on the protective behaviors
            // quizzes.
            var $protectiveBehaviorsQuizzes =
                $('.protective-behaviors,.rate-my-risk');
            if ($protectiveBehaviorsQuizzes.length > 0) {
                return;
            }

            var $form = $('form[method="post"]');
            var $submit = $form.find('input[type="submit"]');

            var me = this;
            $submit.click(function() {
                if (!me.validateRadioButtons($form) ||
                    !me.validateRequiredInputs($form)
                   ) {
                    $form.find('.worth-form-validation-error').hide().fadeIn();
                    return false;
                }
            });
        }
    });

    return QuizValidator;
});
