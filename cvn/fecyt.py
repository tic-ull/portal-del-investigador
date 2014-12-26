# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn

import suds
import base64
import logging

logger = logging.getLogger('cvn')


def pdf2xml(cvn_file):
    try:
        if cvn_file.closed:
            cvn_file.open()
        content = base64.encodestring(cvn_file.read())
    except IOError:
        logger.error(u'No existe el fichero o directorio:' +
                     u' %s' % cvn_file.name)
        return False
    # Web Service - FECYT
    client_ws = suds.client.Client(st_cvn.WS_FECYT_PDF2XML)
    try:
        result_xml = client_ws.service.cvnPdf2Xml(
            st_cvn.USER_FECYT, st_cvn.PASSWORD_FECYT, content)
    except:
        logger.warning(
            u'No hay respuesta del WS' +
            u' de la FECYT para el fichero' +
            u' %s' % cvn_file.name)
        return False, 1
    # Format CVN-XML of FECYT
    if result_xml.errorCode == 0:
        return base64.decodestring(result_xml.cvnXml), 0
    return False, result_xml.errorCode


def xml2pdf(xml):
    content = xml.decode('utf8')
    # Web Service - FECYT
    client_ws = suds.client.Client(st_cvn.WS_FECYT_XML2PDF)
    try:
        pdf = client_ws.service.crearPDFBean(
            st_cvn.USER_FECYT, st_cvn.PASSWORD_FECYT,
            st_cvn.FECYT_CVN_NAME, content, st_cvn.TIPO_PLANTILLA)
    except UnicodeDecodeError as e:
        logger.error(e.message)
        return None
    if pdf.returnCode == '01':
        xml_error = base64.decodestring(pdf.dataHandler)
        logger.error(st_cvn.RETURN_CODE[pdf.returnCode] + u'\n' +
                     xml_error.decode('iso-8859-10'))
        return None
    return base64.decodestring(pdf.dataHandler)
