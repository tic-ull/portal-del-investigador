# -*- encoding: utf-8 -*-
from cvn.utilsCVN import *  # Importación de CVN
from django.core.files.base import ContentFile
from django.contrib import admin, messages
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestInvestcvn, AuthUser
import cvn.settings as cvn_setts    # Constantes para la importación de CVN
import logging

logger = logging.getLogger(__name__)

class AuthUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name',)
    ordering      = ('username',)

class GrupoinvestInvestigadorAdmin(admin.ModelAdmin):
    search_fields = ('nif', 'nombre', 'apellido1', 'apellido2',)
    ordering      = ('apellido1',)

class GrupoinvestInvestcvnAdmin(admin.ModelAdmin):
    actions       = ['pdf_to_xml', 'xml_to_bbdd']
    search_fields = ('investigador__nombre', 'investigador__apellido1', 'investigador__apellido2', 'investigador__nif')
    ordering      = ('fecha_up',)

    def pdf_to_xml(self, request, queryset):
        """ Opción que obtiene la representación XML de los ficheros seleccionados en la plantilla de administración."""
        for qs in queryset:
            xmlFecyt = UtilidadesCVNtoXML(filePDF = qs.cvnfile).getXML()
            if xmlFecyt: # Si el CVN tiene formato FECYT
                # Borramos el viejo para que no se reenumere
                if qs.xmlfile:
                    qs.xmlfile.delete()
                qs.xmlfile.save(qs.cvnfile.name.replace('pdf','xml'), ContentFile(xmlFecyt))
                qs.fecha_cvn = UtilidadesXMLtoBBDD(fileXML = qs.xmlfile).get_fecha_xml()
                qs.save()
                msg = u'La representación XML ' + qs.xmlfile.name + ' se ha obtenido correctamente\n'
                messages.info(request, msg)
                logger.info(msg)
            else:
                msg = u'El CVN "' + qs.cvnfile.name + '" no tiene formato FECYT\n'
                messages.error(request, msg)
                logger.error(msg)


    pdf_to_xml.short_description = u"PDF->XML. Obtener la representación XML de los CVN seleccionados"

    def xml_to_bbdd(self, request, queryset):
        """ Opción que importa los datos de los CVN de los ficheros seleccionados en la plantilla de administración. """
        for qs in queryset:
            cvnFile = qs.cvnfile.name.split('/')[-1]
            qs.fecha_cvn = UtilidadesXMLtoBBDD(fileXML = qs.xmlfile).insertarXML(qs.investigador)
            qs.save()
            msg = u'La inserción en la BBDD del XML ' + qs.xmlfile.name + ' se ha realizado correctamente\n'
            messages.info(request, msg)
            logger.error(msg)

    xml_to_bbdd.short_description = u"XML->BBDD. Importar los datos de los CVN seleccionados a la BBDD local"

# Registrar las tablas en la plantilla administrador
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(GrupoinvestInvestigador, GrupoinvestInvestigadorAdmin)
admin.site.register(GrupoinvestInvestcvn, GrupoinvestInvestcvnAdmin)
