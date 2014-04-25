# -*- encoding: UTF-8 -*-
from cvn import settings as stCVN
import datetime


def parse_scope(treeXML):
    '''Input: Scope node
       Example: CvnItem/Link/Scope'''
    dataCVN = {}
    if treeXML:
        dataCVN['ambito'] = unicode(stCVN.SCOPE[treeXML.find(
            'Type/Item').text.strip()])
        if dataCVN['ambito'] == u'Otros' and treeXML.find('Others/Item'):
            dataCVN['otro_ambito'] = unicode(treeXML.find(
                'Others/Item').text.strip())
    return dataCVN


def parse_duration(duration):
    '''Input: Duration/Item node
       Example: CvnItem/Date/Duration/Item
    '''
    dataCVN = {}
    number = ''
    for item in duration[1:]:
        if item.isdigit():
            number = item
        else:
            if item == 'Y':
                dataCVN['duracion_anyos'] = unicode(number)
            if item == 'M':
                dataCVN['duracion_meses'] = unicode(number)
            if item == 'D':
                dataCVN['duracion_dias'] = unicode(number)
    return dataCVN


def parse_nif(xml):
    '''Input: root node'''
    nif = ''
    id_node = xml.find(
        'Agent/Identification/PersonalIdentification/OfficialId')
    nif_node = id_node.find('DNI/Item')
    if nif_node is None:
        nif_node = id_node.find('NIE/Item')

    if nif_node is not None:
        nif = nif_node.text.strip()

    return nif


def parse_authors(author_list):
    '''Input: A list of Author nodes'''
    authors = ''
    for author in author_list:
        authorItem = ''
        if (author.find("GivenName/Item") and
           author.find("GivenName/Item").text):
            authorItem = unicode(author.find(
                "GivenName/Item").text.strip())
        if (author.find("FirstFamilyName/Item") and
           author.find("FirstFamilyName/Item").text):
            authorItem += u' ' + unicode(author.find(
                "FirstFamilyName/Item").text.strip())
        if (author.find("SecondFamilyName/Item") and
           author.find("SecondFamilyName/Item").text):
            authorItem += u' ' + unicode(
                author.find("SecondFamilyName/Item").text.strip())
        if author.find("Signature/Item").text:
            if authorItem:
                authors += unicode(
                    authorItem + ' (' + author.find(
                        "Signature/Item").text.strip() + '); ')
            else:
                authors += unicode(author.find(
                    "Signature/Item").text.strip() + '; ')
        else:
            authors += authorItem + '; '
    return authors[:-2]


def parse_produccion_type(xml):
    '''Input: CvnItem node'''
    cvn_key = xml.find('CvnItemID/CVNPK/Item').text.strip()
    if not cvn_key in stCVN.FECYT_CODE:
        return ''
    return stCVN.FECYT_CODE[cvn_key]


def parse_produccion_subtype(xml):
    '''Input: CvnItem node'''
    subtype = xml.find('Subtype/SubType1/Item')
    if subtype is None:
        return ''
    subtype = subtype.text.strip()
    if subtype in stCVN.FECYT_CODE_SUBTYPE:
        return stCVN.FECYT_CODE_SUBTYPE[subtype]
    return ''


def parse_publicacion_location(treeXML):
    '''Input: Location node'''
    data = {}
    if treeXML:
        volume = treeXML.find('Volume/Item')
        if volume is not None and volume.text is not None:
            data['volumen'] = volume.text.strip()
        number = treeXML.find('Number/Item')
        if number is not None and number.text is not None:
            data['numero'] = number.text.strip()
        page = treeXML.find('InitialPage/Item')
        if page is not None and page.text is not None:
            data['pagina_inicial'] = page.text.strip()
        page = treeXML.find('FinalPage/Item')
        if page is not None and page.text is not None:
            data['pagina_final'] = page.text.strip()
    return data


def parse_date(xml):
    '''Input: root node'''
    date = xml.find(
        'Version/VersionID/Date/Item').text.strip().split('-')
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))
