# -*- encoding: UTF-8 -*-
from cvn import settings as stCVN


def parse_scope(treeXML):
    dataCVN = {}
    if treeXML:
        dataCVN['ambito'] = unicode(stCVN.SCOPE[treeXML.find(
            'Type/Item').text.strip()])
        if dataCVN['ambito'] == u'Otros' and treeXML.find('Others/Item'):
            dataCVN['otro_ambito'] = unicode(treeXML.find(
                'Others/Item').text.strip())
    return dataCVN


def parse_duration(duration):
    """
         Format: P<num_years>Y<num_months>M<num_days>D
    """
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


def parse_authors(treeXML):
    authors = ''
    for author in treeXML:
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
