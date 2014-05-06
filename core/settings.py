# -*- encoding: UTF-8 -*-

from enum import Enum


# LOG TYPE
class LogType(Enum):
    CVN_STATUS = 0

LOG_TYPE = (
    (LogType.CVN_STATUS, 'CVN_STATUS'),
)
