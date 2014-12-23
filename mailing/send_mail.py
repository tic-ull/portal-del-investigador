# -*- encoding: UTF-8 -*-

from .models import Email
from core import settings as st_core
from core.models import Log
from django.conf import settings as st
from django.template import Template, Context
from mailing import settings as st_mail
from mensajeria import Mensajeria

import datetime
import logging

logger = logging.getLogger('default')


def send_mail(email_type, user, app_label):
    email_to = user.email

    if st.EMAIL_DEBUG:
        email_to = st_mail.EMAIL_DEBUG_ADDRESS

    if email_to is None:
        logger.error(u'El usuario %s (%s) no tiene email asociado' % (
            user.username, user.profile.documento))
        return

    email = Email.objects.get(entry_type=email_type.value)
    if not email.is_active or not email.title or not email.content:
        return

    template = Template(email.content)
    context = Context({})
    content = template.render(context)

    try:
        m = Mensajeria(username=st.MENSAJERIA_USERNAME,
                       password=st.MENSAJERIA_PASSWORD,
                       sender_id=st_mail.EMAIL_SENDER_NAME)

        m.send_email(to=email_to, subject=email.title,
                     body=content, input_html=True)

        Log.objects.create(
            user_profile=user.profile,
            application=app_label.upper(),
            entry_type=st_core.LogType.EMAIL_SENT,
            date=datetime.datetime.now(),
            message=u'[EMAIL: %s] %s' % (
                st_mail.MAIL_TYPE[email.entry_type][1], email.title),
        )
    except Exception as e:
        logger.error('Mensajeria no disponible.' + e.message)
