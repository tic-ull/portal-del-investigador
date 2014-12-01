# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn
from lxml import etree
from datetime import datetime

import time


def get_xml_fragment(filepath):
    xml = open(filepath)
    content = xml.read()
    xml.close()
    return content


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

    def add_teaching_phd(self, title, reading_date,
                         author_first_name, author_last_name,
                         university=st_cvn.UNIVERSITY,
                         codirector_first_name=None, codirector_last_name=''):
        """ Doctoral Thesis Directed """
        teaching_phd = etree.fromstring(get_xml_fragment(
            st_cvn.XML_TEACHING_PHD) % {
                'title': title,
                'reading_date': reading_date.strftime(self.DATE_FORMAT),
                'university': university,
                'first_name': author_first_name,
                'last_name': author_last_name,
            }
        )

        if codirector_first_name is not None:
            title_pos = teaching_phd.index(teaching_phd.find('Title')) + 1
            codirector = get_xml_fragment(
                st_cvn.XML_TEACHING_PHD_CODIRECTOR) % {
                    'codirector_first_name': codirector_first_name,
                    'codirector_last_name': codirector_last_name,
                }
            teaching_phd.insert(title_pos, etree.fromstring(codirector))

        self.xml.append(teaching_phd)

    def add_teaching(self, subject, professional_category, program_type,
                     subject_type, course, qualification, department,
                     faculty, school_year, number_credits,
                     university=st_cvn.UNIVERSITY,):
        '''Graduate, postgraduate (bachelor's degree, master, engineering...)'''
        program_code = self._get_code(st_cvn.FC_PROGRAM_TYPE, program_type)
        subject_code = self._get_code(st_cvn.FC_SUBJECT_TYPE, subject_type)
        teaching = get_xml_fragment(st_cvn.XML_TEACHING) % {
            'subject': subject,
            'professional_category': professional_category,
            'program_type': program_code,
            'subject_type': subject_code,
            'course': course,
            'qualification': qualification,
            'department': department,
            'faculty': faculty,
            'school_year': school_year,
            'number_credits': number_credits,
            'university': university,
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

    def _get_code(self, dic, key):
        try:
            code = dic[key.upper()]
        except KeyError:
            code = u'OTHERS'
        return code

    def _add_other_node(self, xml, code, node):
        value_node = xml.xpath('//Value[@code="' + code + '"]')[-1]
        parent = value_node.getparent()
        parent.insert(parent.index(value_node) + 1, node)

    def add_learning(self, title_name, title_type, university=None, date=None):
        title_code = self._get_code(
            st_cvn.FC_OFFICIAL_TITLE_TYPE, title_type.upper())
        learning = etree.fromstring(get_xml_fragment(
            st_cvn.XML_LEARNING) % {
                'title_name': title_name,
                'title_code': title_code,
                'university': university,
                'date': datetime.strptime(date, '%d/%m/%y').strftime(
                    self.DATE_FORMAT) if date else '2014-01-01',
            }
        )

        if title_code == u'OTHERS':
            node = etree.fromstring(get_xml_fragment(st_cvn.XML_OTHERS) % {
                'code_others': st_cvn.FC_OFFICIAL_UNIVERSITY_TITLE_OTHERS,
                'others': title_type})
            learning.find('Filter').append(node)

        self.xml.append(learning)

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

    def add_learning_phd(self, title, university, date):
        '''PhD (Doctor)'''
        phd_xml = get_xml_fragment(st_cvn.XML_LEARNING_PHD) % {
            'titulo': title, 'centro': university,
            'date': date.strftime(self.DATE_FORMAT)}
        self.xml.append(etree.fromstring(phd_xml))

    def add_learning_other(self, learning_type, title, duration, start_date,
                           end_date):
        other_xml = get_xml_fragment(st_cvn.XML_LEARNING_OTHER) % {
            'title': learning_type + ': ' + title,
            'duration': duration,
            'start_date': start_date.strftime(self.DATE_FORMAT),
            'end_date': end_date.strftime(self.DATE_FORMAT)}
        self.xml.append(etree.fromstring(other_xml))