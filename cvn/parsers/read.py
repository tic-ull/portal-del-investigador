# -*- encoding: UTF-8 -*-

from read_helpers import (parse_date_interval, parse_dedication_type,
                          parse_entities, parse_title, parse_authors,
                          parse_economic, parse_scope, parse_produccion_id,
                          parse_date, parse_publicacion_location, parse_places,
                          parse_filters)
from cvn import settings as st_cvn
import datetime


def _parse_cvnitem_profession(node):
    """Shared parser for current and old profession"""
    date = parse_date_interval(node.find('Date'))
    item = {'title': node.find('Title/Name/Item').text,
            'start_date': date[0],
            'end_date': date[1],
            'full_time': parse_dedication_type(node.find('Dedication/Item'))}
    entities = parse_entities(node.findall('Entity'))
    item['employer'] = (entities[st_cvn.FC_ENTITY.EMPLOYER.value]
                        if entities[st_cvn.FC_ENTITY.EMPLOYER.value] is not None
                        else entities[st_cvn.FC_ENTITY.CURRENT_EMPLOYER.value])
    item['centre'] = (entities[st_cvn.FC_ENTITY.CENTRE.value]
                      if entities[st_cvn.FC_ENTITY.CENTRE.value] is not None
                      else entities[st_cvn.FC_ENTITY.CURRENT_CENTRE.value])
    item['department'] = (entities[st_cvn.FC_ENTITY.DEPT.value]
                          if entities[st_cvn.FC_ENTITY.DEPT.value] is not None
                          else entities[st_cvn.FC_ENTITY.CURRENT_DEPT.value])
    return item


def _parse_cvnitem_scientificexp(node):
    """Shared parser for project and agreement"""
    date_node = node.find('Date')
    date = parse_date_interval(date_node)

    item = {'titulo': parse_title(node),
            'fecha_de_inicio': date[0],
            'fecha_de_fin': date[1],
            'duracion': date[2],
            'autores': parse_authors(node.findall('Author'))}

    item.update(parse_economic(node.findall('EconomicDimension')))
    if node.find('ExternalPK/Code'):
        item[u'cod_segun_financiadora'] = unicode(node.find(
            'ExternalPK/Code/Item').text.strip())
    item.update(parse_scope(node.find('Scope')))
    return item


def parse_cvnitem_scientificexp_project(node):
    return _parse_cvnitem_scientificexp(node)


def parse_cvnitem_scientificexp_agreement(node):
    return _parse_cvnitem_scientificexp(node)


def parse_cvnitem_scientificact_production(node):
    pids = parse_produccion_id(node.findall('ExternalPK'))
    item = {'titulo': parse_title(node),
            'autores': parse_authors(node.findall('Author')),
            'fecha': parse_date(node.find('Date')),
            'issn': pids[st_cvn.PRODUCCION_ID_CODE['ISSN']],
            'isbn': pids[st_cvn.PRODUCCION_ID_CODE['ISBN']],
            'deposito_legal': pids[st_cvn.PRODUCCION_ID_CODE['DEPOSITO_LEGAL']]}
    if (node.find('Link/Title/Name') and
            node.find('Link/Title/Name/Item').text):
        item[u'nombre_publicacion'] = unicode(node.find(
            'Link/Title/Name/Item').text.strip())
    item.update(parse_publicacion_location(node.find('Location')))

    return item


def parse_cvnitem_scientificact_congress(node):
    item = {'titulo': parse_title(node),
            'autores': parse_authors(node.findall('Author'))}

    for itemXML in node.findall('Link'):
        if itemXML.find(
            'CvnItemID/CodeCVNItem/Item'
        ).text.strip() == st_cvn.DATA_CONGRESO:
            if (itemXML.find('Title/Name') and
                    itemXML.find('Title/Name/Item').text):
                item[u'nombre_del_congreso'] = unicode(itemXML.find(
                    'Title/Name/Item').text.strip())

            date_node = itemXML.find('Date')
            (item['fecha_de_inicio'], item['fecha_de_fin'],
                duracion) = parse_date_interval(date_node)

            if itemXML.find('Place/City'):
                item[u'ciudad_de_realizacion'] = unicode(itemXML.find(
                    'Place/City/Item').text.strip())
            # Ámbito
            item.update(parse_scope(itemXML.find('Scope')))
    return item


def parse_cvnitem_scientificexp_property(node):

    places = parse_places(node.findall("Place"))
    entities = parse_entities(node.findall("Entity"))
    num_solicitud = parse_produccion_id(
        node.findall('ExternalPK'))[st_cvn.PRODUCCION_ID_CODE['SOLICITUD']]
    item = {'titulo': parse_title(node),
            'num_solicitud': num_solicitud,
            'lugar_prioritario': places[0],
            'lugares': places[1],
            'autores': parse_authors(node.findall('Author')),
            'entidad_titular': entities[st_cvn.FC_ENTITY.OWNER.value],
            'empresas': entities[st_cvn.FC_ENTITY.OPERATOR.value]}

    dates = node.findall('Date')
    for date in dates:                              # There can be 2 dates
        parsed_date = parse_date(date)
        date_type = date.find("Moment/Item").text
        if date_type == st_cvn.REGULAR_DATE_CODE:   # Date of request
            item['fecha'] = parsed_date
        else:                                       # And date of granting
            item['fecha_concesion'] = parsed_date

    return item


def parse_cvnitem_profession_current(node):
    return _parse_cvnitem_profession(node)


def parse_cvnitem_profession_former(node):
    return _parse_cvnitem_profession(node)


def parse_cvnitem_teaching_phd(node):
    entities = parse_entities(node.findall('Entity'))
    item = {'titulo': parse_title(node),
            'autor': parse_authors(node.findall('Author')),
            'codirector': parse_authors(node.findall('Link/Author')),
            'fecha': parse_date(node.find('Date')),
            'universidad_que_titula': entities[
                st_cvn.FC_ENTITY.PHD_UNIVERSITY.value]}
    return item


def parse_cvnitem_teaching_subject(node):

    entities = parse_entities(node.findall('Entity'))
    filters = parse_filters(node.findall('Filter'))
    item = {'title': node.find('Title/Name/Item').text,
            'course': node.find('Edition/Text/Item').text,
            'qualification': node.find('Link/Title/Name/Item').text,
            'school_year': node.find('Date/StartDate/Year/Item').text,
            'number_credits': node.find('PhysicalDimension/Value/Item').text,
            'university': entities[st_cvn.FC_ENTITY.UNIVERSITY.value],
            'department': entities[st_cvn.FC_ENTITY.TEACHING_DEPARTAMENT.value],
            'faculty': entities[st_cvn.FC_ENTITY.FACULTY.value],
            'program_type': filters[st_cvn.FC_FILTER.PROGRAM.value],
            'subject_type': filters[st_cvn.FC_FILTER.SUBJECT.value]}

    professional_category = node.find('Description/Item').text
    if professional_category is not None:
        item['professional_category'] = professional_category

    return item


def parse_cvnitem_learning_phd(node):
    item = {'title': node.find('Title/Name/Item').text,
            'university': node.find('Entity/EntityName/Item').text,
            'date': parse_date(node.find('Date'))}
    return item


def parse_cvnitem_learning_degree(node):

    title_type = node.find('Filter/Value/Item').text
    if title_type == 'OTHERS':
        title_type = node.find('Filter/Others/Item').text
    else:
        title_type = st_cvn.FC_OFFICIAL_TITLE_TYPE.keys()[
            st_cvn.FC_OFFICIAL_TITLE_TYPE.values().index(unicode(title_type))]
    university = (node.find('Entity/EntityName/Item').text
                  if node.find('Entity/EntityName/Item') is not None
                  else None)
    date = (node.find('Date/OnlyDate/DayMonthYear/Item').text
            if node.find('Date/OnlyDate/DayMonthYear/Item') is not None
            else None)
    try:
        date = datetime.datetime.strptime(date,
                                          st_cvn.XML_CVN_DATE_FORMAT).date()
    except TypeError:
        pass
    item = {'title': node.find('Title/Name/Item').text,
            'title_type': title_type,
            'university': university,
            'date': date}

    return item


def parse_cvnitem(node):
    cvn_key = node.find('CvnItemID/CVNPK/Item').text.strip()
    cvnitem = None
    if cvn_key == st_cvn.CVNITEM_CODE.PROFESSION_CURRENT.value:
        cvnitem = parse_cvnitem_profession_current(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.PROFESSION_FORMER.value:
        cvnitem = parse_cvnitem_profession_former(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.LEARNING_PHD.value:
        cvnitem = parse_cvnitem_learning_phd(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.TEACHING_SUBJECT.value:
        cvnitem = parse_cvnitem_teaching_subject(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.LEARNING_DEGREE.value:
        cvnitem = parse_cvnitem_learning_degree(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.SCIENTIFICEXP_PROPERTY.value:
        cvnitem = parse_cvnitem_scientificexp_property(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.SCIENTIFICEXP_AGREEMENT.value:
        cvnitem = parse_cvnitem_scientificexp_agreement(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.SCIENTIFICEXP_PROJECT.value:
        cvnitem = parse_cvnitem_scientificexp_project(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.TEACHING_PHD.value:
        cvnitem = parse_cvnitem_teaching_phd(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.SCIENTIFICACT_CONGRESS.value:
        cvnitem = parse_cvnitem_scientificact_congress(node)
    elif cvn_key == st_cvn.CVNITEM_CODE.SCIENTIFICACT_PRODUCTION.value:
        cvnitem = parse_cvnitem_scientificact_production(node)
    return cvnitem