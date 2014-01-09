# -*- encoding: utf8 -*-
MESES = (u'enero',
         u'febrero',
         u'marzo',
         u'abril',
         u'mayo',
         u'junio',
         u'julio',
         u'agosto',
         u'septiembre',
         u'octubre',
         u'noviembre',
         u'diciembre')
         
def getMonthText(fecha):
    fecha = str(fecha).split('-')
    mes = int(fecha[1]);
    return MESES[mes]

def cambia_fecha_a_normal(fecha):
    """ 
    entrada YYYY/MM/DD
    salida DD/MM/YYYY
    """
    partes = unicode(fecha).split("-")
    return partes[2] + "/" + partes[1] + "/" + partes[0]

def calcular_duracion(fecha_inicial, anyos, meses, dias):
    """
    devuelve la fecha inicial más los anyos, meses y dias
    """
    from datetime import timedelta
    if not anyos: anyos=0
    if not meses: meses=0
    if not dias: dias=0
    delta_time = timedelta(days=dias + 30 * meses + 365 * anyos)
    return fecha_inicial + delta_time

def utf8(cadena):
    return unicode.encode(cadena, 'utf-8')

