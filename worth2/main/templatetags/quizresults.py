from django import template

register = template.Library()


@register.simple_tag
def is_user_correct(user, question):
    return question.is_user_correct(user)
