'''
Author: Abin Abraham
Template Tag
'''
import re

from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, url):
    """
    Template tag for Menu Active
    example: if home url coming 
    it will check and return active tag
    """
    try:
        pattern = '^%s$' % reverse(url)
    except NoReverseMatch:
        pattern = url

    path = context['request'].path
    return "active" if re.search(pattern, path) else ''