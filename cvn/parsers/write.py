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
                'first_family_name':surnames[0],
                'id_type':st_cvn.FC_OFFICIAL_ID.DNI.name,
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

    def add_phd(self, titulo, centro, date):
        phd_xml = get_xml_fragment(st_cvn.XML_TEACHING_PHD) % {
            'titulo': titulo, 'centro': centro,
            'date': date.strftime(self.DATE_FORMAT)}
        self.xml.append(etree.fromstring(phd_xml))