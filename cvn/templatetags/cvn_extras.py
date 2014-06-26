# -*- encoding: UTF-8 -*-

from cvn import settings as stCVN
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag
def message_waiting(key):
    return mark_safe(stCVN.MESSAGES_WAITING[int(key)])
