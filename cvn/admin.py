# -*- encoding: utf8 -*-
from django.contrib import admin
from cvn.models import (Usuario,
                        Publicacion, Congreso, Proyecto,
                        Convenio, TesisDoctoral,
                        CVN)

class PublicacionCongresoTesisAdmin(admin.ModelAdmin):
    search_fields = ('titulo',
                     'usuario__nombre',
                     'usuario__primer_apellido',
                     'usuario__segundo_apellido',
                     'usuario__documento',)
    ordering = ('created_at',)


class ProyectoConvenioAdmin(admin.ModelAdmin):
    search_fields = ('denominacion_del_proyecto',
                     'usuario__nombre',
                     'usuario__primer_apellido',
                     'usuario__segundo_apellido',
                     'usuario__documento',)
    ordering = ('created_at',)

admin.site.register(Usuario)
# Actividad científica y tecnológica
admin.site.register(Publicacion, PublicacionCongresoTesisAdmin)
admin.site.register(Congreso, PublicacionCongresoTesisAdmin)
admin.site.register(Proyecto, ProyectoConvenioAdmin)
admin.site.register(Convenio, ProyectoConvenioAdmin)
admin.site.register(TesisDoctoral, PublicacionCongresoTesisAdmin)
# Tablas importadas de la aplicación antigua de Viinv
admin.site.register(CVN)
