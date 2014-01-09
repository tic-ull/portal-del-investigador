#!/usr/bin/python
# encoding: utf-8

import time
from datetime import datetime

def datetime_convert(self, time_string):

    # Devuelve una cadena en formato datetime inteligible por django.

    if len(time_string) != 0:
        strp_time = time.strptime(time_string, '%d/%m/%Y %H:%M:%S')
        date_django = datetime.fromtimestamp(time.mktime(strp_time))
        return date_django
    return None


def date_convert(self, time_string):

    # Devuelve una cadena en formato date inteligible por django.

    if len(time_string) != 0:
        date_django = datetime.strptime(time_string, '%d/%m/%Y').strftime('%Y-%m-%d')
        return date_django
    return None


def datetime_to_date(self, date_string):

    # Convierte una cadena datetime en una cadena date

    if len(date_string) != 0:
		date_string = date_string[:10]
        return self.date_convert(date_string)
    return None


def string_to_int(self, int_string):
    #Para aquellos campos del modelo que estan definidos como Integer, puede que en el CSV el valor
    #venga vacío, en esos casos devolvemos un 0.
	return int_string if len(int_string) != 0 else '0'


			
