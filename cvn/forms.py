# -*- coding: utf-8 -*-

from django.forms import ModelForm
from viinvDB.models import GrupoinvestInvestcvn
# Funciones de apoyo
from cvn.helpers import setCVNFileName


class UploadCvnForm(ModelForm):
	""" 
		Formulario que recoge un CVN en formato PDF e introduce sus datos en la BBDD de la aplicación CVN
	"""
			
	class Meta:
		model = GrupoinvestInvestcvn
		fields = ('investigador', 'cvnfile',)

