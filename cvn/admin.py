# -*- encoding: utf8 -*-
from django.contrib import admin
from cvn.models import *

admin.site.register(Usuario)
admin.site.register(SituacionProfesional)

# Actividad científica y tecnológica
admin.site.register(Produccion)
admin.site.register(Publicacion)
admin.site.register(AutorPublicacion)
admin.site.register(Congreso)
admin.site.register(AutorCongreso)

