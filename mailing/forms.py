from django.forms import ModelForm
from django import forms
from django.conf import settings as st

class EmailForm(ModelForm):

    class Meta:
        widgets = {'content': forms.widgets.Textarea(),}

    class Media:
        js = (st.TINYMCE_JS_URL, st.TINYMCE_JS_TEXTAREA)