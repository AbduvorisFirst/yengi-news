from django.db.models import Q
from django.template import Library

register = Library()

@register.filter
def nom(queryset, attrs):
    print('queryset', queryset)
    print('attrs', attrs)

    return queryset