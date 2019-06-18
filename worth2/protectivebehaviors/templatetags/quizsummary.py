from django import template
from quizblock.models import Response, Submission

from worth2.main.views import get_quiz_blocks

register = template.Library()


def get_positive_responses_from_blocks(blocks, user):
    """
    Returns the responses to the quizzes in param 'blocks' that have
    positive values (i.e. greater than 0).

    The returned array is sorted by value, descending.
    """

    positive_answers = []
    for b in blocks:
        # assumption: each of these quiz types has one question
        latest_submission = Submission.objects.filter(
            quiz=b.content_object, user=user).order_by('-submitted').first()

        if latest_submission:
            positive_responses = Response.objects.filter(
                submission=latest_submission, value__gte=1)
            for r in positive_responses:
                positive_answers.append(r)

    sorted_answers = sorted(positive_answers,
                            key=lambda answer: answer.value,
                            reverse=True)
    return sorted_answers


@register.simple_tag
def get_quiz_summary(user, cls):
    """Aggregate a yes/no quiz by collecting all positive responses.

    The Quiz this works on is expected to be implemented as a series of
    pagetree pages. The quiz should use values 1 and 0 for true and
    false.
    """

    return get_positive_responses_from_blocks(get_quiz_blocks(cls), user)


@register.simple_tag
def get_aggregate_level(user, cls):
    """
    Returns the max value for responses for 'user' on pageblocks associated
    with the css class 'cls'.
    """

    responses = get_positive_responses_from_blocks(get_quiz_blocks(cls), user)

    level = 0
    for r in responses:
        level = max(int(r.value), level)

    return int(level)
