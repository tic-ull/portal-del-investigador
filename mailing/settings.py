# -*- encoding: UTF-8 -*-

from enum import IntEnum

MENSAJERIA_USERNAME = '<user>'
MENSAJERIA_PASSWORD = '<password>'
EMAIL_SENDER_NAME = u"Servicio de Investigación"
EMAIL_DEBUG_ADDRESS = 'stic.becariosinvestigacion.info@ull.edu.es'


class MailType(IntEnum):
    EXPIRED = 0

MAIL_TYPE = (
    (MailType.EXPIRED.value, 'EXPIRED'),
)

# ************************* SETTINGS LOCAL ***********************************
try:
    MAILING_SETTINGS_LOCAL
except NameError:
    try:
        from .settings_local import *
    except ImportError:
        pass
# ************************* SETTINGS LOCAL ***********************************
