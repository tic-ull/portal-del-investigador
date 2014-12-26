# -*- encoding: UTF-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from string import Template


class FileFieldURLWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        if value:
            tpl = Template(u"<a href='%s'>%s</a>" % (value.url, value.name))
            return mark_safe(tpl.template)
