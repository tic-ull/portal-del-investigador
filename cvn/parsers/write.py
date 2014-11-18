# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn
from lxml import etree

import time


def get_xml_fragment(path):
    f = open(path)
    xml = f.read()
    f.close()
    return xml


class CvnXmlWriter:

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, user, *args, **kwargs):
        xml = kwargs.pop('xml', None)
        if xml is not None:
            self.xml = etree.fromstring(xml)
            self.xml.find(
                'Version/VersionID/Date/Item'
            ).text = time.strftime(self.DATE_FORMAT)
        else:
            if user.profile.documento[0].isdigit():
                documento = st_cvn.FC_OFFICIAL_ID.DNI
            else:
                documento = st_cvn.FC_OFFICIAL_ID.NIE
            xml = get_xml_fragment(st_cvn.XML_SKELETON_PATH) % {
                'today': time.strftime(self.DATE_FORMAT),
                'version': st_cvn.WS_FECYT_VERSION,
                'given_name': user.first_name,
                'first_family_name': user.last_name,
                'id_type': documento.name,
                'id_type_code': documento.value,
                'official_id': user.profile.documento,
                'internet_email_address': user.email
            }
            self.xml = etree.fromstring(xml.encode('utf8'))

    def tostring(self):
        return etree.tostring(self.xml)

    def add_teaching_phd(self, title, university, reading_date, signature,
                     given_name, first_family_name, second_family_name=None):
        teaching = etree.fromstring(get_xml_fragment(
            st_cvn.XML_TEACHING) % {
                'title': title,
                'university': university,
                'reading_date': reading_date.strftime(self.DATE_FORMAT),
                'given_name': given_name,
                'first_family_name': first_family_name,
                'signature': signature
            }
        )
        self.xml.append(teaching)

    def add_learning(self, title_name, university, date, title_type):
        '''Graduate, postgraduate (bachelor's degree, master, engineering...)'''
        code = self._get_code(st_cvn.FC_OFFICIAL_TITLE_TYPE, title_type)
        academic_education = etree.fromstring(get_xml_fragment(
            st_cvn.XML_BACHELOR_ENGINEERING) % {
                'title': title_name,
                'university': university,
                'date': date.strftime(self.DATE_FORMAT),
                'code': code
            }
        )
        if code == u'OTHERS':
            node = etree.fromstring(get_xml_fragment(st_cvn.XML_OTHERS) % {
                'code_others': st_cvn.FC_OFFICIAL_UNIVERSITY_TITLE_OTHERS,
                'others': title_type})
            academic_education.find('Filter').append(node)
        self.xml.append(academic_education)

    def add_profession(self, title, employer, start_date, end_date=None,
                       centre=None, department=None, full_time=None):
        values_xml = {'title': title,
                      'employer': employer,
                      'start_date': start_date.strftime(self.DATE_FORMAT)}
        if end_date:
            xml_path = st_cvn.XML_PROFESSION
            values_xml['end_date'] = end_date.strftime(self.DATE_FORMAT)
        else:
            xml_path = st_cvn.XML_CURRENT_PROFESSION
        profession_xml = get_xml_fragment(xml_path) % values_xml
        profession = etree.fromstring(profession_xml)

        # If it is specified if the job is full or partial time
        if full_time is not None:
            dedication_type = (st_cvn.FC_DEDICATION_TYPE.TOTAL.value
                               if full_time else
                               st_cvn.FC_DEDICATION_TYPE.PARTIAL.value)
            full_time_xml = get_xml_fragment(st_cvn.XML_DEDIACTION) % {
                'code': (st_cvn.FC_PROFESSION_CODE.CURRENT_TRIMMED.value
                         if end_date is None else
                         st_cvn.FC_PROFESSION_CODE.OLD_TRIMMED.value),
                'type': dedication_type}
            profession.append(etree.fromstring(full_time_xml))

        entity_pos = profession.index(profession.find('Entity')) + 1

        # If it is specified the department where the job takes place
        if department is not None:
            entity_type = (st_cvn.FC_ENTITY.CURRENT_DEPARTMENT.value
                           if end_date is None else
                           st_cvn.FC_ENTITY.DEPARTMENT.value)
            department_xml = get_xml_fragment(st_cvn.XML_ENTITY) % {
                'code': entity_type,
                'name': department}
            profession.insert(entity_pos, etree.fromstring(department_xml))

        # If it is specified the centre (building) where the job takes place
        if centre is not None:
            entity_type = (st_cvn.FC_ENTITY.CURRENT_CENTRE.value
                           if end_date is None else
                           st_cvn.FC_ENTITY.CENTRE.value)
            centre_xml = get_xml_fragment(st_cvn.XML_ENTITY) % {
                'code': entity_type,
                'name': centre}
            profession.insert(entity_pos, etree.fromstring(centre_xml))

        self.xml.append(profession)

    def add_learning_phd(self, titulo, centro, date):
        '''PhD (Doctor)'''
        phd_xml = get_xml_fragment(st_cvn.XML_TEACHING_PHD) % {
            'titulo': titulo, 'centro': centro,
            'date': date.strftime(self.DATE_FORMAT)}
        self.xml.append(etree.fromstring(phd_xml))

    def _get_code(self, dic, data_type):
        try:
            code = dic[data_type.upper()]
        except KeyError:
            code = u'OTHERS'
        return code

    def _add_other_node(self, xml, code, node):
        value_node = xml.xpath('//Value[@code="' + code + '"]')[-1]
        pi = value_node.getparent()
        pi.insert(pi.index(value_node) + 1, node)

    def add_teaching(self, subject, program_type, subject_type, course,
                     qualification, department, faculty, start_date,
                     number_credits):
        program_code = self._get_code(st_cvn.FC_PROGRAM_TYPE, program_type)
        subject_code = self._get_code(st_cvn.FC_SUBJECT_TYPE, subject_type)
        teaching = get_xml_fragment(st_cvn.XML_TEACHING) % {
            'subject': subject,
            'program_type': program_code,
            'subject_type': subject_code,
            'course': course,
            'qualification': qualification,
            'department': department,
            'faculty': faculty,
            'start_date': start_date.strftime(self.DATE_FORMAT),
            'number_credits': number_credits
        }
        self.xml.append(etree.fromstring(teaching))
        if program_code == u'OTHERS':
            node = etree.fromstring(get_xml_fragment(st_cvn.XML_OTHERS) % {
                'code_others': st_cvn.FC_PROGRAM_TYPE_OTHERS,
                'others': program_type})
            self._add_other_node(self.xml, st_cvn.FC_PROGRAM, node)
        if subject_code == u'OTHERS':
            node = etree.fromstring(get_xml_fragment(st_cvn.XML_OTHERS) % {
                'code_others': st_cvn.FC_SUBJECT_TYPE_OTHERS,
                'others': subject_type})
            self._add_other_node(self.xml, st_cvn.FC_SUBJECT, node)

    def add_learning_other(self, type, title, duration, start_date, end_date):
        other_xml = get_xml_fragment(st_cvn.XML_LEARNING_OTHER) % {
            'title': type + ': ' + title,
            'duration': duration,
            'start_date': start_date.strftime(self.DATE_FORMAT),
            'end_date': end_date.strftime(self.DATE_FORMAT)}
        self.xml.append(etree.fromstring(other_xml))