# -*- encoding: UTF-8 -*-

from enum import IntEnum


class LogType(IntEnum):
    CVN_STATUS = 0
    AUTH_ERROR = 1
    EMAIL_SENT = 2

LOG_TYPE = (
    (LogType.CVN_STATUS.value, 'CVN_STATUS'),
    (LogType.AUTH_ERROR.value, 'AUTH_ERROR'),
    (LogType.EMAIL_SENT.value, 'EMAIL_SENT'),
)
