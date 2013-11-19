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
    actions       = ['getAdminXML', 'parseAdminPDF']
    search_fields = ('investigador__nombre', 'investigador__apellido1', 'investigador__apellido2', 'investigador__nif')
    ordering      = ('fecha_up',)

    def getAdminXML(self, request, queryset):
        """ Opción que obtiene la representación XML de los ficheros seleccionados en la plantilla de administración."""
        for qs in queryset:
            xmlFecyt = UtilidadesCVNtoXML(filePDF = qs.cvnfile).getXML()
            if xmlFecyt: # Si el CVN tiene formato FECYT
                qs.xmlfile.save(qs.cvnfile.name.replace('pdf','xml'), ContentFile(xmlFecyt))
                qs.fecha_cvn = UtilidadesXMLtoBBDD(fileXML = qs.xmlfile).insertarXML(qs.investigador)
                qs.save()
                msg = u'La representación XML' + qs.xmlfile.name + ' se ha obtenido correctamente\n'
                messages.info(request, msg)
                logger.info(msg)
            else:
                msg = u'El CVN "' + qs.cvnfile.name + '" no tiene formato FECYT\n'
                messages.error(request, msg)
                logger.error(msg)
                

    getAdminXML.short_description = u"Obtener la representación XML de los CVN seleccionados"

    def parseAdminPDF(self, request, queryset):
        """ Opción que importa los datos de los CVN de los ficheros seleccionados en la plantilla de administración. """

        inicial = datetime.datetime.now()
        for cvn in queryset:
            cvnFile = cvn.cvnfile.name.split('/')[-1]
            currentXML = UtilidadesXMLtoBBDD(fileXML = cvnFile.replace("pdf", "xml"))
            # Retorna el usuario que se ha introducido en la BBDD
            currentXML.parseXML()#fileBBDD, fileCVN)
        final     = datetime.datetime.now()
        print "Tiempo finalización: " + str(final)
        diff_time = final - inicial
        print "Minutos: " + str(int(diff_time.total_seconds()/60.0))
        print "Segundos: " + str(int(diff_time.total_seconds()%60.0))

    parseAdminPDF.short_description = u"Importar los datos de los CVN seleccionados a la BBDD local"

# Registrar las tablas en la plantilla administrador
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(GrupoinvestInvestigador, GrupoinvestInvestigadorAdmin)
admin.site.register(GrupoinvestInvestcvn, GrupoinvestInvestcvnAdmin)
