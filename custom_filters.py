from django import template

register = template.Library()

@register.filter
def is_any_opened_duration(task, user):
    return task.is_any_opened_duration(user)