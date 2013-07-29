# -*- coding: utf-8 -*-

from django.forms import ModelForm
from viinvDB.models import GrupoinvestInvestcvn

# Funciones de apoyo
from cvn.helpers import setCVNFileName

from django.contrib.admin.widgets import AdminFileWidget
from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django import forms

#
from django.forms.widgets import ClearableFileInput
import os
# missing imports
from django.utils.safestring import mark_safe
from cgi import escape
from django.utils.encoding import force_unicode

class ShortNameClarableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': '',
            'input_text': '',
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        
        template = u'%(input)s'
                
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)
        
        if value and hasattr(value, "url"):
            template = self.template_with_initial            
            
            substitutions['initial'] = (u'<a href="%s" target>%s</a>'
                                        % (escape(value.url),
                                           escape(force_unicode('')))) # I just changed this line
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions
        #return mark_safe(template % substitutions)
        string = template % substitutions        
        return mark_safe(string.replace(':','').replace('<br />',''))
        
        


class UploadCvnForm(ModelForm):
	""" 
		Formulario que recoge un CVN en formato PDF e introduce sus datos en la BBDD de la aplicación CVN
	"""
	# TODO: Eliminar cuando en el modelo original se quite la restricción de 'blank=True' en dicho campo.
	#~ cvnfile = forms.FileField()
	
	class Meta:
		model = GrupoinvestInvestcvn		
		widgets = {			
			'cvnfile': ShortNameClarableFileInput,
		}
		fields = ('cvnfile',) #'investigador'	




	

