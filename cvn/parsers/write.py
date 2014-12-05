# -*- encoding: UTF-8 -*-

from cvn import settings as st_cvn
from lxml import etree

import time


def get_xml_fragment(filepath):
    xml = open(filepath)
    content = xml.read()
    xml.close()
    return content


class CvnXmlWriter:

    DATE_FORMAT = st_cvn.XML_CVN_DATE_FORMAT

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

    def _get_code(self, dic, key):
        try:
            code = dic[key.upper()]
        except KeyError:
            code = u'OTHERS'
        return code

    def _add_other_node(self, xml, code, node):
        value_node = xml.xpath('//Value[@code="' + code + '"]')
        if len(value_node):
            parent = value_node[-1].getparent()
            parent.insert(parent.index(value_node[-1]) + 1, node)

    def _remove_node(self, xml, node):
        node = xml.find(node)
        xml.remove(node)

    def _remove_parent_node_by_code(self, xml, node, code):
        nodes = xml.xpath('//%s[@code="%s"]' % (node, code))
        if len(nodes):
            node = nodes[0].getparent()
            xml.remove(node)

    def add_teaching(self, subject, professional_category, program_type,
                     subject_type, course, qualification, department,
                     faculty, school_year, number_credits,
                     university=st_cvn.UNIVERSITY,):
        """Graduate, postgraduate (bachelor's degree, master, engineering...)"""
        program_code = self._get_code(st_cvn.FC_PROGRAM_TYPE, program_type)
        subject_code = self._get_code(st_cvn.FC_SUBJECT_TYPE, subject_type)
        teaching = etree.fromstring(get_xml_fragment(
            st_cvn.XML_TEACHING) % {
                'subject': subject,
                'professional_category': professional_category,
                'program_type': program_code,
                'subject_type': subject_code,
                'course': course,
                'qualification': qualification,
                'department': department,
                'faculty': faculty,
                'school_year': school_year,
                'number_credits': number_credits.replace(',', '.'),
                'university': university,
            }
        )

        if university is None:
            self._remove_parent_node_by_code(
                xml=teaching, node='EntityName',
                code=st_cvn.FC_ENTITY.UNIVERSITY.value)

        if department is None:
            self._remove_parent_node_by_code(
                xml=teaching, node='EntityName',
                code=st_cvn.FC_ENTITY.TEACHING_DEPARTAMENT.value)

        if faculty is None:
            self._remove_parent_node_by_code(
                xml=teaching, node='EntityName',
                code=st_cvn.FC_ENTITY.FACULTY.value)

        self.xml.append(teaching)

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

    def add_learning(self, title_name, title_type, university=None, date=None):
        title_code = self._get_code(
            st_cvn.FC_OFFICIAL_TITLE_TYPE, title_type.upper())
        learning = etree.fromstring(get_xml_fragment(
            st_cvn.XML_LEARNING) % {
                'title_name': title_name,
                'title_code': title_code,
                'university': university,
                'date': date.strftime(self.DATE_FORMAT) if date else None,
            }
        )

        if date is None:
            self._remove_node(learning, 'Date')

        if university is None:
            self._remove_node(learning, 'Entity')

        if title_code == u'OTHERS':
            node = etree.fromstring(get_xml_fragment(st_cvn.XML_OTHERS) % {
                'code_others': st_cvn.FC_OFFICIAL_UNIVERSITY_TITLE_OTHERS,
                'others': title_type})
            learning.find('Filter').append(node)

        self.xml.append(learning)

    def add_learning_phd(self, title, date=None, university=st_cvn.UNIVERSITY):
        """ PhD (Doctor) """
        learning_phd = etree.fromstring(get_xml_fragment(
            st_cvn.XML_LEARNING_PHD) % {
                'title': title,
                'university': university,
                'date': date.strftime(self.DATE_FORMAT) if date else None,
            }
        )

        if date is None:
            self._remove_node(learning_phd, 'Date')

        if university is None:
            self._remove_node(learning_phd, 'Entity')

        self.xml.append(learning_phd)

    def add_profession(self, title, start_date, employer=st_cvn.UNIVERSITY,
                       end_date=None, centre=None, department=None,
                       full_time=None):
        values = {'title': title,
                  'start_date': start_date.strftime(self.DATE_FORMAT),
                  'employer': employer,
                  'centre': centre,
                  'department': department,
                  'full_time': full_time,
                  'dedication_code': None,
                  'dedication_type': None,
                  }

        if full_time is not None:
            values['dedication_code'] = (
                st_cvn.FC_PROFESSION_CODE.CURRENT_TRIMMED.value
                if end_date is None else
                st_cvn.FC_PROFESSION_CODE.OLD_TRIMMED.value)

            values['dedication_type'] = (
                st_cvn.FC_DEDICATION_TYPE.TOTAL.value
                if full_time else
                st_cvn.FC_DEDICATION_TYPE.PARTIAL.value)

        xml = st_cvn.XML_CURRENT_PROFESSION
        if end_date is not None:
            values['end_date'] = end_date.strftime(self.DATE_FORMAT)
            xml = st_cvn.XML_PROFESSION

        profession = etree.fromstring(get_xml_fragment(xml) % values)

        if centre is None:
            centre_code = (st_cvn.FC_ENTITY.CURRENT_CENTRE.value
                           if end_date is None else
                           st_cvn.FC_ENTITY.CENTRE.value)
            self._remove_parent_node_by_code(
                xml=profession, node='EntityName', code=centre_code)

        if department is None:
            department_code = (st_cvn.FC_ENTITY.CURRENT_DEPT.value
                               if end_date is None else
                               st_cvn.FC_ENTITY.DEPT.value)
            self._remove_parent_node_by_code(
                xml=profession, node='EntityName', code=department_code)

        if full_time is None:
            self._remove_node(xml=profession, node='Dedication')

        self.xml.append(profession)