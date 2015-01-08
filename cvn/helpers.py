# -*- encoding: UTF-8 -*-

import datetime
import hashlib
import os


# Do not touch. Uses self so it can be called in a django upload_to field
# https://stackoverflow.com/questions/17539720/django-model-with-filefield-dynamic-upload-to-argument
def get_md5_path(self):
    md5 = hashlib.md5(self.user_profile.documento).hexdigest()[0:2]
    return "cvn/%s/" % md5


# Do not touch. Uses self so it can be called in a django upload_to field
# https://stackoverflow.com/questions/17539720/django-model-with-filefield-dynamic-upload-to-argument
def get_cvn_path(self, filename):
    return os.path.join(
        get_md5_path(self), self.user_profile.documento, filename)


# Do not touch. Uses self so it can be called in a django upload_to field
# https://stackoverflow.com/questions/17539720/django-model-with-filefield-dynamic-upload-to-argument
def get_old_cvn_path(self, filename):
    return os.path.join(
        get_md5_path(self), self.user_profile.documento, 'old', filename)


class DateRange:
    MIN_DATE = datetime.date(datetime.MINYEAR, 1, 1)
    MAX_DATE = datetime.date(datetime.MAXYEAR, 12, 31)

    def __init__(self, start_date=None, end_date=None):
        self.start_date = self.MIN_DATE if start_date is None else start_date
        self.end_date = self.MAX_DATE if end_date is None else end_date

    def intersect(self, b):
        return ((self.start_date <= b.start_date <= self.end_date)
                or (b.start_date <= self.start_date <= b.end_date))
