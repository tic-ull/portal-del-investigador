# -*- encoding: UTF-8 -*-

from enum import IntEnum


class MailType(IntEnum):
    EXPIRED = 0

MAIL_TYPE = (
    (MailType.EXPIRED.value, 'EXPIRED'),
)