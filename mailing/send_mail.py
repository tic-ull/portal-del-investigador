# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from django.template import Template, Context
import logging
from mailing.models import Email
import mailing.settings as st_mail
from mensajeria import Mensajeria

logger = logging.getLogger('default')


def send_mail(email_code, email_to):
    email = Email.objects.get(entry_type=email_code.value)
    if not email.title or not email.content:
        return
    template = Template(email.content)
    context = Context({})
    content = template.render(context)
    if st.EMAIL_DEBUG:
        email_to = st_mail.EMAIL_DEBUG_ADDRESS
    m = Mensajeria(username=st_mail.MENSAJERIA_USERNAME,
                   password=st_mail.MENSAJERIA_PASSWORD,
                   sender_id=st_mail.EMAIL_SENDER_NAME)
    m.send_email(to=email_to,
                 subject=email.title,
                 body=content,
                 input_html=True)