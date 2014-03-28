# -*- encoding: UTF-8 -*-

from cvn.models import (Usuario, Congreso, Proyecto, Convenio,
                        TesisDoctoral, Articulo, Libro,
                        CVN, Capitulo)
from django.contrib import admin


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
admin.site.register(Articulo, PublicacionCongresoTesisAdmin)
admin.site.register(Libro, PublicacionCongresoTesisAdmin)
admin.site.register(Capitulo, PublicacionCongresoTesisAdmin)
admin.site.register(Congreso, PublicacionCongresoTesisAdmin)
admin.site.register(Proyecto, ProyectoConvenioAdmin)
admin.site.register(Convenio, ProyectoConvenioAdmin)
admin.site.register(TesisDoctoral, PublicacionCongresoTesisAdmin)
admin.site.register(CVN)
