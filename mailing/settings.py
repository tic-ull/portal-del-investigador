# -*- encoding: UTF-8 -*-

from enum import IntEnum

EMAIL_DEBUG_ADDRESS = 'stic.becariosinvestigacion.info@ull.edu.es'
EMAIL_SENDER_NAME = u"Servicio de Investigación"
MENSAJERIA_USERNAME = ""
MENSAJERIA_PASSWORD = ""


class MailType(IntEnum):
    EXPIRED = 0

MAIL_TYPE = (
    (MailType.EXPIRED.value, 'EXPIRED'),
)