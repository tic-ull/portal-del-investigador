# -*- encoding: UTF-8 -*-

from enum import IntEnum

EMAIL_SENDER_NAME = u"Servicio de Investigación"
EMAIL_DEBUG_ADDRESS = 'stic.becariosinvestigacion.info@ull.edu.es'


class MailType(IntEnum):
    EXPIRED = 0

MAIL_TYPE = (
    (MailType.EXPIRED.value, 'EXPIRED'),
)
