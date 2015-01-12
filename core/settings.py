# -*- encoding: UTF-8 -*-

from enum import IntEnum


class LogType(IntEnum):
    """
    CVN_STATUS:     writes to db cvn.status field when cvn.status is updated
    CVN_UPDATED:    writes to db cvn.status, cvn.uploaded_at and cvn.fecha every
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
