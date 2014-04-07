# -*- encoding: UTF-8 -*-

from cvn.models import (UserProfile, Congreso, Proyecto, Convenio,
                        TesisDoctoral, Articulo, Libro,
                        CVN, Capitulo)
from django.contrib import admin

import logging

logger = logging.getLogger(__name__)


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


class CVNAdmin(admin.ModelAdmin):
    actions = ['pdf_to_xml', 'xml_to_bbdd']
    search_fields = ('usuario__user__first_name', 'usuario__user__last_name',
                     'usuario__documento',)
    ordering = ('updated_at',)

    '''
    def pdf_to_xml(self, request, queryset):
        for qs in queryset:
            xmlFecyt = UtilidadesCVNtoXML(filePDF=qs.cvn_file).getXML()
            if xmlFecyt:  # Formato FECYT
                if qs.xml_file:
                    # Borra el viejo para que no se reenumere
                    qs.xml_file.delete()
                qs.xml_file.save(qs.cvn_file.name.replace('pdf', 'xml'),
                                ContentFile(xmlFecyt))
                qs.fecha_cvn = UtilidadesXMLtoBBDD(fileXML=qs.xml_file)\
                    .getXMLDate()
                qs.save()
                msg = u'La representación XML ' + qs.xml_file.name + \
                    ' se ha obtenido correctamente\n'
                messages.info(request, msg)
                logger.info(msg)
            else:
                msg = u'El CVN "' + qs.cvn_file.name + \
                    '" no tiene formato FECYT\n'
                messages.error(request, msg)
                logger.error(msg)

    pdf_to_xml.short_description = u"PDF->XML. Obtener la representación XML \
         de los CVN-PDF seleccionados"


    def xml_to_bbdd(self, request, queryset):
        for qs in queryset:
            util = UtilidadesXMLtoBBDD(fileXML=qs.xml_file)
            util.insertarXML(qs.usuario.user)
            qs.fecha_cvn = util.getXMLDate()
            qs.save()
            msg = u'La inserción en la BBDD del XML ' + qs.xml_file.name + \
                ' se ha realizado correctamente\n'
            messages.info(request, msg)
            logger.error(msg)

    xml_to_bbdd.short_description = u"XML->BBDD. Importar los datos de \
        los CVN-XML seleccionados a la BBDD local"
    '''

admin.site.register(UserProfile)
admin.site.register(Articulo, PublicacionCongresoTesisAdmin)
admin.site.register(Libro, PublicacionCongresoTesisAdmin)
admin.site.register(Capitulo, PublicacionCongresoTesisAdmin)
admin.site.register(Congreso, PublicacionCongresoTesisAdmin)
admin.site.register(Proyecto, ProyectoConvenioAdmin)
admin.site.register(Convenio, ProyectoConvenioAdmin)
admin.site.register(TesisDoctoral, PublicacionCongresoTesisAdmin)
admin.site.register(CVN, CVNAdmin)
