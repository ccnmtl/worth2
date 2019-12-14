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
         * This function returns false if all the checkboxes on the
         * form that has class `cssClass` (default: 'quizblock-required')
         * are unchecked. Otherwise, it returns true.
         */
        validateCheckboxForm: function($form, cssClass) {
            if (typeof cssClass === 'undefined') {
                cssClass = 'quizblock-required';
            }

            var $requiredCheckboxes = $form
                .find('.' + cssClass)
                .find('input[type="checkbox"]');

            if ($requiredCheckboxes.length > 0) {
                var hasAnyCheckedCheckboxes = _.reduce(
                    $requiredCheckboxes,
                    function(memo, $el) {
                        var grpName = $($el).attr('name');
                        var grp = $('input:checkbox[name="' + grpName + '"]');
                        return memo && $(grp).is(':checked');
                    },
                    true);

                if ($requiredCheckboxes.length > 0 &&
                    !hasAnyCheckedCheckboxes
                ) {
                    return false;
                }
            }

            return true;
        },

        /**
         * This function returns false if all the radio buttons on the
         * form are unchecked. Otherwise, it returns true.
         */
        validateRadioButtons: function($form) {
            var $radioButtons = $form.find('input[type="radio"]');
            var hasAnyCheckedRadioButtons = _.reduce(
                $radioButtons,
                function(memo, $el) {
                    var grpName = $($el).attr('name');
                    var grp = $('input:radio[name="' + grpName + '"]');
                    return memo && $(grp).is(':checked');
                },
                true);

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
        validateRequiredTextInputs: function($form, cssClass) {
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
            // quizzes or the goal setting and checkin forms
            var query = '.protective-behaviors,.rate-my-risk,' +
                '.goal-setting,.goal-check-in';
            if ($(query).length > 0) {
                return;
            }

            var $form = $('form[method="post"]');
            if ($form.find('input[name="action"]').val() === 'reset') {
                // This is the "I want to change my answers" form, so don't
                // validate it.
                return;
            }

            var me = this;
            var $next = $('#next-page');
            var $submit = $form.find('input[type="submit"]');

            $next.click(function() {
                if (!me.validateCheckboxForm($form) ||
                    !me.validateRadioButtons($form) ||
                    !me.validateRequiredTextInputs($form)
                ) {
                    $form.find('.alert').hide();
                    $form.find('.worth-form-validation-error').fadeIn();
                    return false;
                }

                if ($submit.length > 0) {
                    $form.find('.alert').hide();
                    $form.find('.worth-form-submit-prompt').fadeIn();
                    return false;
                }
            });

            $submit.click(function() {
                if (!me.validateCheckboxForm($form) ||
                    !me.validateRadioButtons($form) ||
                    !me.validateRequiredTextInputs($form)
                ) {
                    $form.find('.alert').hide();
                    $form.find('.worth-form-validation-error').fadeIn();
                    return false;
                }
            });
        }
    });

    return QuizValidator;
});
