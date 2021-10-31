from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name="times")
def times(number):
    """A way to create for loop with range in
    Django Template Engine. Returns array of numbers."""
    return range(number)


@register.simple_tag
def url_replace(request, field, value):
    """Used by pagination to add GET param."""
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
