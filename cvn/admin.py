# -*- encoding: UTF-8 -*-

from cvn.models import (Usuario, Publicacion, Congreso, Proyecto, Convenio,
                        TesisDoctoral, Articulo, Libro, Capitulo)
from django.contrib import admin


class UsuarioAdmin(admin.ModelAdmin):
    search_fields = ('documento',
                     'nombre',
                     'primer_apellido',
                     'segundo_apellido',
                     'documento',)
    ordering = ('created_at',)


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

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Publicacion, PublicacionCongresoTesisAdmin)
admin.site.register(Articulo, PublicacionCongresoTesisAdmin)
admin.site.register(Libro, PublicacionCongresoTesisAdmin)
admin.site.register(Capitulo, PublicacionCongresoTesisAdmin)
admin.site.register(Congreso, PublicacionCongresoTesisAdmin)
admin.site.register(Proyecto, ProyectoConvenioAdmin)
admin.site.register(Convenio, ProyectoConvenioAdmin)
admin.site.register(TesisDoctoral, PublicacionCongresoTesisAdmin)
