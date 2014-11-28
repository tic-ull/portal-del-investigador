# -*- encoding: UTF-8 -*-

from random import randint
from factory.fuzzy import FuzzyDate
import random


class ProfessionFactory:

    @staticmethod
    def create():
        fd = FuzzyDate()
        d = {'title': 'Titulo ' + randint(0, 100),
             'employer': 'Empresa ' + randint(0, 100),
             'start_date': fd.start_date}
        if random.choice([True, False]):
            d['end_date'] = fd.end_date
        if random.choice([True, False]):
            d['centre'] = 'Centro ' + randint(0, 100)
        if random.choice([True, False]):
            d['department'] = 'Departamento ' + randint(0, 100)
        if random.choice([True, False]):
            d['full_time'] = random.choice([True, False])
        return d


class TeachingPhdFactory:

    @staticmethod
    def create():
        fd = FuzzyDate()
        d = {'title': 'Titulo ' + randint(0, 100),
             'reading_date': fd.start_date,
             'author_first_name': random.choice(['Cacerolo', 'Espinacia',
                                                 'Caralampio', 'Diodora']),
             'author_last_name': u'Rodríguez' + random.choice([u' Martín', ''])}

        if random.choice([True, False]):
            d['university'] = 'Universidad #' + randint(0, 100)
        if random.choice([True, False]):
            d['codirector_first_name'] = 'Aceitunio'
        if random.choice([True, False]):
            d['codirector_last_name'] = (u'Rodríguez' +
                                         random.choice([u' Martín', '']))
        return d


class LearningOtherFactory:

    @staticmethod
    def create():
        fd = FuzzyDate()
        return {'type': random.choice(['Curso', 'Conferencia', 'Taller']),
             'title': 'Titulo #' + randint(0, 100),
             'duration': randint(1, 100),
             'start_date': fd.start_date,
             'end_date': fd.end_date}


class LearningPhdFactory:

    @staticmethod
    def create():
        fd = FuzzyDate()
        return {'title': 'Titulo #' + randint(0, 100),
             'university': 'Universidad #' + randint(0, 100),
             'date': fd.start_date}