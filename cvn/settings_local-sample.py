# -*- encoding: UTF-8 -*-

CVN_SETTINGS_LOCAL = True
from .settings import *

# Enable translations in this file
_ = lambda s: s

# Default Entity
UNIVERSITY = _(u'Universidad de La Laguna')

# Expiry date for a CVN
EXPIRY_DATE = datetime.date(2013, 12, 31)

# WS FECYT
FECYT_USER = "user"
FECYT_PASSWORD = "password"

# Unauthorized CVN Authors
CVN_PDF_AUTHOR_NOAUT = [u'FECYT - Author of Example', ]
