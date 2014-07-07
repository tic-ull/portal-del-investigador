# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag
def messages_waiting():
    html = "switch($key) {\n"
    for i in range(len(st_cvn.MESSAGES_WAITING) - 1):
        html += ("\t" * 6 + "case %s:\n" % i)
        html += ("\t" * 7 + "$('#show').text(\"" +
                 st_cvn.MESSAGES_WAITING[i] + "\");\n")
        html += ("\t" * 7 + "break;\n")
    html += (
        "\t" * 6 + "default:\n" +
        "\t" * 7 + "$('#show').text(\"" +
        st_cvn.MESSAGES_WAITING.values()[-1] + "\");\n" +
        "\t" * 5 + "}")
    return mark_safe(html)
