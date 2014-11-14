# -*- encoding: UTF-8 -*-

import cvn.settings as st_cvn
from lxml import etree


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
        else:
            surnames = user.last_name.split(' ')

            xml = get_xml_fragment(st_cvn.XML_SKELETON_PATH) % {
                'given_name': user.first_name,
                'first_family_name': surnames[0],
                'id_type': st_cvn.FC_OFFICIAL_ID.DNI.name,
                'id_type_code': st_cvn.FC_OFFICIAL_ID.DNI.value,
                'official_id': user.profile.documento,
                'internet_email_address': user.email
            }
            self.xml = etree.fromstring(xml.encode('utf8'))
            if len(surnames) == 2:
                first_surname = self.xml.find('Agent/Identification/Personal'
                                              'Identification/FirstFamilyName')
                self._append_2nd_surname(first_surname, surnames[1],
                                         st_cvn.FC_SURNAME.APELLIDO.value)

    def tostring(self):
        return etree.tostring(self.xml)

    @staticmethod
    def _append_2nd_surname(surname_node, second_surname, code):
        second_surname_node = etree.fromstring(get_xml_fragment(
            st_cvn.XML_2ND_SURNAME) % {
                'second_family_name': second_surname, 'code': code})
        pi = surname_node.getparent()
        pi.insert(pi.index(surname_node) + 1, second_surname_node)

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
        if second_family_name is not None:
            first_surname = teaching.find('Author/FirstFamilyName')
            self._append_2nd_surname(first_surname, second_family_name,
                                     st_cvn.FC_SURNAME.DOCTORANDO.value)
        self.xml.append(teaching)

    def add_learning(self, title, university, date, code,
                                 title_type = None):
        '''Graduate, postgraduate (bachelor's degree, master, engineering...)'''
        academic_education = etree.fromstring(get_xml_fragment(
            st_cvn.XML_BACHELOR_ENGINEERING) % {
                'title': title,
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

    def add_profession(self, prof_name, employer, start_date, end_date=None):
        values_xml = {'profession': prof_name,
                      'employer': employer,
                      'start_date': start_date.strftime(self.DATE_FORMAT)}
        if end_date:
            xml_path = st_cvn.XML_PROFESSION
            values_xml['end_date'] = end_date.strftime(self.DATE_FORMAT)
        else:
            xml_path = st_cvn.XML_CURRENT_PROFESSION
        profession_xml = get_xml_fragment(xml_path) % values_xml
        self.xml.append(etree.fromstring(profession_xml))

    def add_learning_phd(self, titulo, centro, date):
        '''PhD (Doctor)'''
        phd_xml = get_xml_fragment(st_cvn.XML_TEACHING_PHD) % {
            'titulo': titulo, 'centro': centro,
            'date': date.strftime(self.DATE_FORMAT)}
        self.xml.append(etree.fromstring(phd_xml))

    def _get_code_teaching(self, dic, data_type):
        try:
            code = dic[data_type]
        except KeyError:
            code = u'OTHERS'
        return code

    def _create_other_node(self, xml_skeleton, code_others, others):
        return etree.fromstring(get_xml_fragment(xml_skeleton) % {
            'code_others': code_others,
            'others': others
        })

    def _add_other_node(self, xml, code, node):
        value_node = xml.xpath('//Value[@code="' + code + '"]')[-1]
        pi = value_node.getparent()
        pi.insert(pi.index(value_node) + 1, node)

    def add_teaching(self, subject, program_type, subject_type, course,
                     qualification, department, faculty, start_date,
                     number_credits):
        program_code = self._get_code_teaching(st_cvn.FC_PROGRAM_TYPE,
                                               program_type)
        subject_code = self._get_code_teaching(st_cvn.FC_SUBJECT_TYPE,
                                               subject_type)
        teaching = get_xml_fragment(st_cvn.XML_TEACHING) % {
            'subject': subject,
            'program_type': program_code,
            'subject_type': subject_code,
            'course': course,
            'qualification': qualification,
            'department': department,
            'faculty': faculty,
            'start_date': start_date,
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