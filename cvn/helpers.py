# -*- encoding: UTF-8 -*-

import hashlib
import os


def get_md5_path(self):
    md5 = hashlib.md5(self.user_profile.documento).hexdigest()[0:2]
    return "cvn/%s/" % md5


def get_cvn_path(self, filename):
    return os.path.join(
        get_md5_path(self), self.user_profile.documento, filename)
