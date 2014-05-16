# -*- encoding: UTF-8 -*-

from enum import Enum


# LOG TYPE
class LogType(Enum):
    CVN_STATUS = 0
    AUTH_ERROR = 1

LOG_TYPE = (
    (LogType.CVN_STATUS, 'CVN_STATUS'),
    (LogType.AUTH_ERROR, 'AUTH_ERROR'),
)
