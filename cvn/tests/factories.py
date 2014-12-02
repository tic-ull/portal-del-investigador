# -*- encoding: UTF-8 -*-

from random import randint
from cvn import settings as st_cvn
import random
import datetime


def fuzzy_date():
    start = datetime.date(randint(1940, 2040), randint(1, 12), randint(1, 28))
    end = datetime.date(randint(start.year, 2040), randint(start.month, 12),
                        randint(start.day, 28))
    return [start, end]

class ProfessionFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        d = {'title': 'Titulo ' + str(randint(0, 100)),
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


class TeachingPhdFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        d = {'title': 'Titulo ' + str(randint(0, 100)),
             'reading_date': fd[0],
             'author_first_name': random.choice(['Cacerolo', 'Espinacia',
                                                 'Caralampio', 'Diodora']),
             'author_last_name': u'Rodríguez' + random.choice([u' Martín', ''])}

        if random.choice([True, False]):
            d['university'] = 'Universidad #' + str(randint(0, 100))
        if random.choice([True, False]):
            d['codirector_first_name'] = 'Aceitunio'
        if random.choice([True, False]):
            d['codirector_last_name'] = (u'Rodríguez' +
                                         random.choice([u' Martín', '']))
        return d


class LearningOtherFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        return {'type': random.choice(['Curso', 'Conferencia', 'Taller']),
             'title': 'Titulo #' + str(randint(0, 100)),
             'duration': str(randint(1, 100)),
             'start_date': fd[0],
             'end_date': fd[1]}


class LearningPhdFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        return {'title': 'Titulo #' + str(randint(0, 100)),
                'university': 'Universidad #' + str(randint(0, 100)),
                'date': fd[0]}


class TeachingFactory:

    @staticmethod
    def create():
        program_type = u'Titulación #' + str(randint(0, 100))
        if random.choice([True, False]):
            program_type = random.choice(st_cvn.FC_PROGRAM_TYPE.keys())
        subject_type = 'Tipo asignatura #' + str(randint(0, 100))
        if random.choice([True, False]):
            subject_type = random.choice(st_cvn.FC_SUBJECT_TYPE.keys())
        return {'subject': 'Asignatura #' + str(randint(0, 100)),
                'professional_category': u'Profesión #' + str(randint(0, 100)),
                'program_type': program_type,
                'subject_type': subject_type,
                'course': randint(0, 5),
                'qualification': random.choice(['',
                                                u'Titulación #' +
                                                str(randint(0, 100))]),
                'department': random.choice(['', 'Departamento #' +
                                             str(randint(0, 100))]),
                'faculty': random.choice(['', 'Facultad #' +
                                          str(randint(0, 100))]),
                'school_year': randint(1990, 2020),
                'number_credits': format(random.uniform(0, 20), '.1f'),
                'university': random.choice(['', st_cvn.UNIVERSITY,
                                             'Universidad #' +
                                             str(randint(0, 100))]),
                }


class LearningFactory:

    @staticmethod
    def create():
        fd = fuzzy_date()
        fd.append(None)
        pass
