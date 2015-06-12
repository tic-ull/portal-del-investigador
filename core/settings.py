# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015
#
#      STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Portal del Investigador is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Portal del Investigador.  If not, see
#    <http://www.gnu.org/licenses/>.
#

from django.conf import settings as st
from enum import IntEnum

# Enable translations in this file
_ = lambda s: s


class LogType(IntEnum):
    """
    CVN_STATUS:  writes to db cvn.status field when cvn.status is updated
    CVN_UPDATED: writes to db cvn.status, cvn.uploaded_at and cvn.fecha every
                 time the cvn is updated
    """
    CVN_STATUS = 0  # This type is not used currently. We now use CVN_UPDATED
    AUTH_ERROR = 1
    EMAIL_SENT = 2
    CVN_UPDATED = 3

LOG_TYPE = (
    (LogType.CVN_STATUS.value, 'CVN_STATUS'),
    (LogType.AUTH_ERROR.value, 'AUTH_ERROR'),
    (LogType.EMAIL_SENT.value, 'EMAIL_SENT'),
    (LogType.CVN_UPDATED.value, 'CVN_UPDATED'),
)

st.CONSTANCE_CONFIG['SITEWIDE_WARNING'] = ('', _('Warning Message to show on every page (leave empty to disable)'))