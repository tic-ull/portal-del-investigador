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


def _parse_duration(duration):
    '''Input: Duration/Item node
       Example: CvnItem/Date/Duration/Item
    '''
    duration = duration.text
    duracion = 0
    number = ''
    for item in duration[1:]:
        if item.isdigit():
            number = item
        else:
            if item == 'Y':
                duracion += int(unicode(number)) * 365
            if item == 'M':
                duracion += int(unicode(number)) * 30
            if item == 'D':
                duracion += int(unicode(number))
    return duracion


def parse_nif(xml):
    '''Input: root node'''
    if xml is None:
        return ''
    nif = ''
    id_node = xml.find(
        'Agent/Identification/PersonalIdentification/OfficialId')
    if id_node is None:
        return nif
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
    if xml is None:
        return ''
    cvn_key = xml.find('CvnItemID/CVNPK/Item').text.strip()
    if cvn_key not in stCVN.FECYT_CODE:
        return ''
    return stCVN.FECYT_CODE[cvn_key]


def parse_produccion_subtype(xml):
    '''Input: CvnItem node'''
    if xml is None:
        return ''
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


def _parse_segregated_date(xml):
    date = xml.find('DayMonthYear/Item')
    if date is not None:
        date = date.text.split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))
    date = xml.find('MonthYear/Item')
    if date is not None:
        date = date.text.split('-')
        return datetime.date(int(date[0]), int(date[1]), 1)
    date = xml.find('Year/Item')
    if date is not None:
        return datetime.date(int(date.text), 1, 1)
    return None


def _parse_unitary_date(xml):
    date = xml.text.split('-')
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))


def parse_date(xml):
    '''Input: date node'''
    if xml is None:
        return None
    # Node of type Date > OnlyDate
    node = xml.find('OnlyDate')
    if node is not None:
        return _parse_segregated_date(node)
    # Node of type Date > StartDate
    node = xml.find('StartDate')
    if node is not None:
        return _parse_segregated_date(node)
    # Node of type Date > Item
    node = xml.find('Item')
    if node is not None:
        return _parse_unitary_date(node)
    return None


def parse_date_interval(xml):
    '''Input: date node'''
    if xml is None:
        return None, None, None
    # Get start date
    fecha_inicio = parse_date(xml)
    fecha_fin_1 = None
    fecha_fin_2 = None
    duration_1 = 0
    duration_2 = 0
    # Get end date
    node = xml.find('EndDate')
    if node is not None:
        fecha_fin_1 = _parse_segregated_date(node)
        '''If fecha_inicio is None duration is useless. So in the case
           of being a fecha_fin with no fecha inicio we just return it.'''
        if fecha_inicio is None:
            return None, fecha_fin_1, None
        delta = fecha_fin_1 - fecha_inicio
        duration_1 = delta.days
    # Get duration
    node = xml.find('Duration/Item')
    if node is not None:
        duration_2 = _parse_duration(node)
        if fecha_inicio is None:
            return None, None, None
        fecha_fin_2 = fecha_inicio + datetime.timedelta(days=duration_2)
    # Chose what end date to return. The first if is needed so fecha_fin
    # is None instead of equal to fecha_inicio in certain conditions.
    if fecha_fin_1 is None and fecha_fin_2 is None:
        return fecha_inicio, None, None
    if duration_1 > duration_2:
        return fecha_inicio, fecha_fin_1, duration_1
    else:
        return fecha_inicio, fecha_fin_2, duration_2


def parse_produccion_id(id_list, code_type):
    '''Input: id_list is a list of ExternalPK nodes (ExternalPK nodes contain
       different identifiers for produccion nodes. code_type is what
       type of id you want to get: ISSN, ISBN, etc. (PRODUCCION_ID_CODE)'''
    for node in id_list:
        if node.find('Type/Item').text != code_type:
            continue
        return node.find('Code/Item').text
    return None
