# -*- encoding: UTF-8 -*-

from random import randint
from cvn import settings as st_cvn
import random
import datetime
import factory
from factory.fuzzy import (FuzzyChoice, FuzzyDate, FuzzyAttribute)

d = datetime.date(1940, 1, 1)


class ProfessionFactory(factory.Factory):
    FACTORY_FOR = dict
    title = factory.Sequence(lambda n: 'Trabajo #{0}'.format(n))
    employer = FuzzyAttribute(lambda: 'Empresa #' + str(randint(0, 100)))
    start_date = FuzzyDate(datetime.date(1940, 1, 1)).fuzz()
    end_date = FuzzyAttribute(lambda: random.choice(
        [None, FuzzyDate(d).fuzz()]))
    centre = FuzzyAttribute(lambda: random.choice(
        [None, 'Centro #' + str(randint(0, 100))]))
    department = FuzzyAttribute(lambda: random.choice(
        [None, 'Departamento #' + str(randint(0, 100))]))
    full_time = FuzzyChoice([True, False, None])


class LearningPhdFactory(factory.Factory):
    FACTORY_FOR = dict
    title = factory.Sequence(lambda n: 'PHD recibido #{0}'.format(n))
    university = FuzzyAttribute(lambda: 'Universidad #' + str(randint(0, 100)))
    date = FuzzyAttribute(lambda: random.choice([None, FuzzyDate(d).fuzz()]))


class TeachingFactory:

    @staticmethod
    def create():
        program_type = u'Titulación #' + str(randint(0, 100))
        if random.choice([True, False]):
            program_type = random.choice(st_cvn.FC_PROGRAM_TYPE.keys())
        subject_type = 'Tipo asignatura #' + str(randint(0, 100))
        if random.choice([True, False]):
            subject_type = random.choice(st_cvn.FC_SUBJECT_TYPE.keys())
        d = {'subject': 'Asignatura #' + str(randint(0, 100)),
             'program_type': program_type,
             'subject_type': subject_type,
             'course': str(randint(0, 5)),
             'qualification': u'Titulación #' + str(randint(0, 100)),
             'faculty': 'Facultad #' + str(randint(0, 100)),
             'school_year': randint(1990, 2020),
             'number_credits': format(random.uniform(0, 20), '.1f'),
            }
        # Optional data
        if random.choice([True, False]):
            d['department'] = 'Departamento #' + str(randint(0, 100))
        if random.choice([True, False]):
            d['professional_category'] = u'Profesión #' + str(randint(0, 100))
        if random.choice([True, False]):
            d['university'] = random.choice(
                [st_cvn.UNIVERSITY, 'Universidad #' + str(randint(0, 100))])
        return d


class LearningFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        fd.append(None)
        return {'title': u'Título #' + str(randint(0, 100)),
                'title_type': random.choice(
                    st_cvn.FC_OFFICIAL_TITLE_TYPE.keys()),
                'university': random.choice([
                    None, 'Universidad #' + str(randint(0, 100))]),
                'date': random.choice(fd),
                }
