# -*- coding: utf-8 -*-

# BBDD de Viinv
from viinvDB.models import GrupoinvestInvestigador, GrupoinvestInvestcvn, AuthUser, GrupoinvestCategoriainvestigador
from cvn.models import *
from django.contrib.auth.models import User

# Parsear XML
from lxml import etree

# Excepción para la búsqueda de objetos en la BBDD
from django.core.exceptions import ObjectDoesNotExist

# Constantes para la importación de CVN
import cvn.settings as cvn_setts

# Expresiones regulares
import re
import os
#~ # Mover los ficheros duplicados a históricos
import shutil
# Fechas
from dateutil.relativedelta import relativedelta
import datetime
# Cálculo del hash
import hashlib


# Fichero con funciones auxiliares para las vistas
# ------------------------------------------------

def formatNIF(data = None):
    """ 
    Función de ayuda que recibe un dato (NIE - NIF) y lo formatea para poder realizar
    las búsquedas. El formateo consiste en eliminar:
      * guiones "-"
      * puntos "." 
    
    Variables:
    - data: Documento de identificación a formatear.
    """
    # Eliminar guiones del documento de identificacion
    if not data:
        return None
    # Eliminar espacios al principio o al final de la cadena
    return data.upper().replace(' ', '').replace('-', '').replace('.', '')  
        

def searchDataUser(data = None):
    """
        Función que devuelve un diccionario para buscar los datos de un usuario en la BBDD.
        Su principal uso es para comprobar que no se va a añadir un usuario que ya existe.
        Si el usuario dispone de NIF/NIE, es el único parámetro que se usa para la búsqueda
        
        Variables:
        - data:  Diccionario con los datos personales del usuario a añadir.
        
        Return: Diccionario de búsqueda.
    """
    search_dic = {} 
    if data.has_key('documento'):
        search_dic['documento__icontains'] = data['documento']
    else:
        if data.has_key('segundo_apellido'):
            search_dic['segundo_apellido'] = data['segundo_apellido']
        if data.has_key('primer_apellido'):
            search_dic['primer_apellido__iexact'] = data['primer_apellido']
        if data.has_key('nombre'):
            search_dic['nombre__iexact'] = data['nombre']       
    return search_dic
    
    
def formatCode(data, extension):
    """
        Función que transforma el código de una etiqueta para realizar las comprobaciones de datos a analizar.
        Por ejemplo, en las publicaciones se repite varias veces la etiqueta "Title" en el mismo nivel del árbol.
        Para diferenciarlas el XML añade un atributo "code", el cual sólo varía en la última cifra respecto al código
        CVNPK que inidica el tipo de Actividad Científica que se está analiczando.
        
        Variables:
        - data: Contiene el código del tipo de Actividad Científica a analizar.
        - extension: Indica el tipo de código a añadir al código de la tabla.
        
        Return: El código correspondiente a buscar en el atributo de la etiqueta.
    """
    data = data.split(".")
    data[-1] = extension
    data = ".".join(data)
    return data
    
    
def searchDataProduccionCientifica(data = None):
    """
        Función que devuelve un diccionario para buscar los datos de la producción científica
        en la BBDD.
        
        Variables:
        - data: Diccionario con los datos de la producción científica       
        
        Return: Diccionario de búsqueda.
    """
    # NOTE sólo se busca por un parámetro, pues puede darse el caso en el que dos registros iguales, en uno
    #      se tenga más datos de búsqueda y no encuentre dicho elemento ya insertado    
    search_dic = {}
    # Denominación del proyecto: Proyectos y Convenios 
    if data.has_key('denominacion_del_proyecto'):
        search_dic['denominacion_del_proyecto__iexact'] = data['denominacion_del_proyecto']
    # Título: Publicacion, Congreso y TesisDoctoral
    elif data.has_key('titulo'):
        search_dic['titulo__iexact'] = data['titulo']
    return search_dic
    
    
def formatDate(date = ""):
    """
        Recibe una fecha formada sólo por el año y la transforma a una fecha con mes y día.
        Se establece por defecto el 1 de Enero del año recibido
        
        Variables:
        - date: Dato que contiene la fecha 
    """
    date += "-1-1"
    return date


def checkPage(data = ""):
    """
        Comprueba si la página introducida contiene "-" o " ". En tal caso se devuelve (-1)
        para indicar que el dato ha sido introducido pero el formato no es correcto.
        
        Variables:
        - data: Página inicial o final      
    """
    try:
        checkData = int(data)
    except ValueError: # Encuentra algún símbolo extraño
        return cvn_setts.INVALID_PAGE
    except TypeError:  # El Item viene vacío
        return cvn_setts.INVALID_PAGE
    return data 
    

def setCVNFileName(user):
    """
        Añade el nombre del usuario y una clave al nombre del fichero antes de almacenarlo.
    """
    obfusc = str(hashlib.md5(str(19 * int(user.id) + 5235)).hexdigest())[2:10]
    return 'CVN-' + str(user.user.username) + '-' + obfusc + u'.pdf'
    
    
def handleOldCVN(cvnName = None, cvn = None):
    """
        Función que se encarga de escribir los CVNs antiguos en el directorio de histórico añadiendo
        en el nombre del mismo la fecha de subida.  
        
        Variables:
        - cvnName: Nombre del CVN antiguo a modificar.
        - cvn: Datos del cvn antiguo
    """
    
    if cvnName is not None:         
        # Antes de mover a la carpeta históricos, se le añade la fecha de subida al CVN nuevo.
        cvnfile = cvnName.split('/')[-1]
        cvnfile = cvnfile.split('.')[0]
        cvnfile += u'-' + str(cvn.fecha_up) + u'.pdf'   
        # Comprobar que la ruta del fichero no sea la de la aplicación antigua.
        if 'cvn' in cvnName.split('/'):
            cvnName = cvn_setts.URL_PDF + cvnName.split('/')[-1]            
        shutil.move(cvnName, cvn_setts.URL_OLD_CVN + cvnfile)


def getUserViinV(documento = ""):
    """
        Función que a partir del usuario CAS devuelve los datos almacenados en Viinv.
        
        Variables:
        - documento: NIF/NIE del usuario CAS
    """ 
    invest        = None
    investCVN     = None
    investCVNname = None    
    try:
        invest = GrupoinvestInvestigador.objects.get(nif = documento)       
        investCVN     = GrupoinvestInvestcvn.objects.get(investigador = invest) 
        investCVNname = investCVN.cvnfile.name
    except GrupoinvestInvestigador.DoesNotExist:
        pass
    except GrupoinvestInvestcvn.DoesNotExist:
        pass
    return invest, investCVN, investCVNname 
    

def addUserViinV(data = {}):
    """
        Función que añade a ViinV al usuario logueado por CAS si no existe.
        
        Variables:
        - data: Datos del usuario logeado por CAS
        
        {'username': 'lcerrudo', 'first_name': 'LUIS MARINO', 'last_name': 'CERROD CONCEPCION', 
        'TipoDocumento': 'NIF', 'NumDocumento': '42185973V', 
        'ou': ['PDI', 'srv_wifi', 'Alumnos', 'srv_soft', 'rol_becario', 'srv_webpages', 'srv_ddv', 
               'srv_vpn', 'CCTI', 'srv_siga_ull.es', 'NACFicheros', 'Act', 'srv_google', 'srv_siga'],
        'email': 'lcerrudo@ull.edu.es'}
    """ 
    if data:
        user = User.objects.db_manager('portalinvestigador').create_user(username=data['username'], password='', email=data['email'])       
        data_invest = {}
        data_invest['nombre'] = data['first_name']
        apellidos = data['last_name'].split(' ')
        try:
            data_invest['apellido1'] = apellidos[0]
            data_invest['apellido2'] = apellidos[1]
        except IndexError:
            data_invest['apellido2'] = ''
        data_invest['nif'] = data['NumDocumento']
        data_invest['email'] = data['email']
        # Los siguientes datos no vienen en el CAS, hay un demonio que lo corrige luego a través de los datos de RRHH
        data_invest['sexo'] = 'Hombre'
        data_invest['categoria'] = GrupoinvestCategoriainvestigador.objects.get(nombre='INVES')
        data_invest['cod_persona'] = 'INVES'
        # FIXME: En la última versión de la BBDD de ViinV este campo no es obligatorio, ACTUALIZAR
        data_invest['dedicacion'] = ''
        data_invest['user'] = AuthUser.objects.get(username = data['username'])
        invest = GrupoinvestInvestigador.objects.create(**data_invest)
        return invest
        
    
def getDataCVN(data = ""):
    """
        Función que devuelve un diccionario con los datos a mostrar del CVN del usuario.
        
        Variables:
        - data: NIF/NIE del usuario.
    """
    context = {}
    context['CVN'] = True   
    try:
        user = Usuario.objects.get(documento__icontains = data) 
        print user
        context['Publicaciones'] = Publicacion.objects.filter(usuario = user).order_by('-fecha', 'titulo')
        context['Congresos'] = Congreso.objects.filter(usuario = user).order_by('-fecha_realizacion', 'titulo')
        context['Proyectos'] = Proyecto.objects.filter(usuario = user).order_by('-fecha_de_inicio', 'denominacion_del_proyecto')
        context['Convenios'] = Convenio.objects.filter(usuario = user).order_by('-fecha_de_inicio', 'denominacion_del_proyecto')
        context['TesisDoctorales'] = TesisDoctoral.objects.filter(usuario = user).order_by('-fecha_de_lectura', 'titulo')
    except ObjectDoesNotExist:
        context['CVN'] = False
    return context
    



    
def dataCVNSession(investCVN = None):
    """
        Función que devuelve los datos relevante del CVN del usuario que acaba de acceder a la aplicación.
        
        Retorna un diccionario con los datos:
        - Fecha de creación del CVN.
        - Fichero que contiene el CVN <- Modificado, ahora se realiza en la vista 'downloadCVN'
        - Necesidad de actualizar el CVN.
        - Fecha hasta cuando es válido
    """
    context = {}
    context['fecha_cvn'] = investCVN.fecha_cvn
    # Comprobar si el CVN no se ha actualizado en 6 meses   
    #~ context['file_cvn'] = investCVN.cvnfile  
    # NOTE: En los ficheros subidos desde la nueva aplicación no hace falta modificar la ruta.  
    #~ context['file_cvn'].name = cvn_setts.MEDIA_PDF +investCVN.cvnfile.name.split('/')[-1]    
    #~ if (investCVN.fecha_cvn + datetime.timedelta(days = cvn_setts.CVN_CADUCIDAD)) < datetime.date.today():
    if (investCVN.fecha_cvn + relativedelta(years = cvn_setts.CVN_CADUCIDAD)) < datetime.date.today():
        context['updateCVN'] = True
    else:               
        #~ context['fecha_valido'] = investCVN.fecha_cvn + datetime.timedelta(days = cvn_setts.CVN_CADUCIDAD)
        context['fecha_valido'] = investCVN.fecha_cvn + relativedelta(years = cvn_setts.CVN_CADUCIDAD)              
    return context
        
