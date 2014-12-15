# -*- encoding: UTF-8 -*-

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
