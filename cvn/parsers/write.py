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
            others_node = etree.fromstring(get_xml_fragment(
                st_cvn.XML_OTHERS_TITLE) % {'others': title_type}
            )
            academic_education.find('Filter').append(others_node)
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

    def add_learning_other(self, type, title, duration, start_date, end_date):
        other_xml = get_xml_fragment(st_cvn.XML_LEARNING_OTHER) % {
            'title': type + ': ' + title,
            'duration': duration,
            'start_date': start_date.strftime(self.DATE_FORMAT),
            'end_date': end_date.strftime(self.DATE_FORMAT)}
        self.xml.append(etree.fromstring(other_xml))