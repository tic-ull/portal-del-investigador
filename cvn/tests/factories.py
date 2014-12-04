# -*- encoding: UTF-8 -*-

from random import randint
from cvn import settings as st_cvn
import random
import datetime
import itertools

it = itertools.count()

def fuzzy_date():
    start = datetime.date(randint(1940, 2040), randint(1, 12), randint(1, 28))
    end = datetime.date(randint(start.year, 2040), randint(start.month, 12),
                        randint(start.day, 28))
    return [start, end]


class ProfessionFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        d = {'title': 'Trabajo #' + str(it.next()),
             'employer': 'Empresa ' + str(randint(0, 100)),
             'start_date': fd[0]}
        if random.choice([True, False]):
            d['end_date'] = fd[1]
        if random.choice([True, False]):
            d['centre'] = 'Centro ' + str(randint(0, 100))
        if random.choice([True, False]):
            d['department'] = 'Departamento ' + str(randint(0, 100))
        if random.choice([True, False]):
            d['full_time'] = random.choice([True, False])
        return d


class LearningPhdFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        d = {'title': 'PHD recibido #' + str(it.next()),
             'university': 'Universidad #' + str(randint(0, 100))}
        if random.choice([True, False]):
            d['date'] = fd[0]
        return d


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