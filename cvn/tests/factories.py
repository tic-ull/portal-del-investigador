# -*- encoding: UTF-8 -*-

from random import randint, uniform
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


class TeachingFactory(factory.Factory):
    FACTORY_FOR = dict
    title = factory.Sequence(lambda n: 'Asignatura #{0}'.format(n))
    professional_category = FuzzyAttribute(
        lambda: u'Profesión #' + str(randint(0, 100)))
    program_type = FuzzyAttribute(lambda: random.choice(
        st_cvn.FC_SUBJECT_TYPE.keys() +
        [u'Titulación #' + str(randint(0, 100))]))
    subject_type = FuzzyAttribute(lambda: random.choice(
        st_cvn.FC_SUBJECT_TYPE.keys() +
        ['Tipo asignatura #' + str(randint(0, 100))]))
    course = FuzzyAttribute(lambda: str(randint(1, 5)))
    qualification = factory.Sequence(lambda n: u'Titulación #{0}'.format(n))
    university = FuzzyAttribute(lambda: random.choice(
        [None, st_cvn.UNIVERSITY, 'Universidad #' + str(randint(0, 100))]))
    department = FuzzyAttribute(lambda: random.choice(
        [None, 'Departamento #' + str(randint(0, 100))]))
    faculty = FuzzyAttribute(lambda: random.choice(
        [None, 'Facultad #' + str(randint(0, 100))]))
    school_year = FuzzyAttribute(lambda: str(randint(1990, 2020)))
    number_credits = FuzzyAttribute(lambda: str(round(uniform(0.5, 15.5), 2)))


class LearningFactory(factory.Factory):
    FACTORY_FOR = dict
    title = factory.Sequence(lambda n: u'Título #{0}'.format(n))
    title_type = FuzzyAttribute(lambda: random.choice(
        st_cvn.FC_OFFICIAL_TITLE_TYPE.keys() + ['GRADO', 'FP']))
    university = FuzzyAttribute(lambda: random.choice(
        [None, 'Universidad #' + str(randint(0, 100))]))
    date = FuzzyAttribute(lambda: random.choice(
        [None, FuzzyDate(d).fuzz()]))