# -*- encoding: UTF-8 -*-

from random import randint
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