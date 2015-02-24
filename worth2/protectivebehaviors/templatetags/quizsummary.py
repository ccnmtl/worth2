from django import template
from quizblock.models import Response, Submission

from worth2.main.views import get_quiz_blocks

register = template.Library()


class PositiveQuizResponses(template.Node):
    """Aggregate a yes/no quiz by collecting all positive responses.

    The Quiz this works on is expected to be implemented as a series of
    pagetree pages. The quiz should use values 1 and 0 for true and
    false.
    """

    def __init__(self, user, quiz_class, var_name):
        self.user = user
        self.quiz_class = quiz_class
        self.var_name = var_name

    def render(self, context):
        u = context[self.user]
        cls = context[self.quiz_class]

        blocks = get_quiz_blocks(cls)

        positive_answers = []
        for b in blocks:
            # assumption: each of these quiz types has one question
            latest_submission = Submission.objects.filter(
                quiz=b.content_object, user=u).order_by('-submitted').first()

            if latest_submission:
                positive_responses = Response.objects.filter(
                    submission=latest_submission, value__gte=1)
                for r in positive_responses:
                    positive_answers.append(r)

        sorted_answers = sorted(positive_answers,
                                key=lambda answer: answer.value,
                                reverse=True)
        context[self.var_name] = sorted_answers
        return ''


@register.tag('get_quiz_summary')
def quizsummary(parser, token):
    user = token.split_contents()[1:][0]
    quiz_class = token.split_contents()[1:][1]
    var_name = token.split_contents()[1:][3]
    return PositiveQuizResponses(user, quiz_class, var_name)
