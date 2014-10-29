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
                second_surname = etree.fromstring(get_xml_fragment(
                    st_cvn.XML_2ND_SURNAME) %
                        {'second_family_name': surnames[1]})
                first_surname = self.xml.find('Agent/Identification/Personal'
                                              'Identification/FirstFamilyName')
                pi = first_surname.getparent()
                pi.insert(pi.index(first_surname) + 1, second_surname)

    def tostring(self):
        return etree.tostring(self.xml)

    def add_profession(self, profession_name, employer, start_date, end_date):
        profession = etree.fromstring(get_xml_fragment(
            st_cvn.XML_PROFESSION) % {
                'profession': profession_name,
                'employer': employer,
                'start_date': start_date.strftime(self.DATE_FORMAT),
                'end_date': end_date.strftime(self.DATE_FORMAT)
        })
        self.xml.append(profession)

    def add_teaching(self, data):
        teaching = etree.fromstring(get_xml_fragment(
            st_cvn.XML_TEACHING) % {
                'title': data['title'],
                'university': data['university'],
                'reading_date': data['reading_date'].strftime(self.DATE_FORMAT),
                'given_name': data['given_name'],
                'first_family_name': data['first_family_name'],
                'second_family_name': data['second_family_name'],
                'signature': data['signature']
            }
        )
        self.xml.append(teaching)

    def _official_title_(self, type):
        if type == u'Doctor':
            return st_cvn.OFFICIAL_TITLE_TYPE.T_DOC.value
        if type == u'Licenciado/Ingeniero Superior':
            return st_cvn.OFFICIAL_TITLE_TYPE.T_SUP.value
        if type == u'Diplomado/Ingeniero Tecnico':
            return st_cvn.OFFICIAL_TITLE_TYPE.T_MED.value
        return u'OTHERS'


    def add_bachelor_engineering(self, data):
        others = ''
        try:
            if data['type'] is not None:
                code = self._official_title_(data['type'])
                if code == u'OTHERS':
                    others = data['type']
        except KeyError:
            code = ''
        academic_education = etree.fromstring(get_xml_fragment(
            st_cvn.XML_BACHELOR_ENGINEERING) % {
                'title': data['title'],
                'university': data['university'],
                'date': data['date'].strftime(self.DATE_FORMAT),
                'code': code,
                'others': others
            }
        )
        node = academic_education.find('Filter')
        if code != u'OTHERS':
            node.remove(node.find('Others'))
        if not code:
            academic_education.remove(node)
        self.xml.append(academic_education)
