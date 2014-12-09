# -*- encoding: UTF-8 -*-

from random import randint
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
