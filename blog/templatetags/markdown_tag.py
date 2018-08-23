import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def djangomarkdown(value):
    return mark_safe(markdown2.markdown(force_str(value),
                                        extras=["code-friendly"]
                                        ))