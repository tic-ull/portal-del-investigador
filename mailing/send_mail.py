# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from django.core.mail import EmailMessage
from smtplib import SMTPRecipientsRefused
from django.template import Template, Context
import logging
from mailing.models import Email
import mailing.settings as st_mail

logger = logging.getLogger('default')


def send_mail(email_code, email_to):
    email = Email.objects.get(entry_type=email_code.value)
    template = Template(email.content)
    context = Context({})
    content = template.render(context)
    if st.EMAIL_DEBUG:
        email_to = st_mail.EMAIL_DEBUG_ADDRESS
    msg = EmailMessage(subject=email.title, body=content, to=[email_to])
    msg.content_subtype = "html"  # Main content is now text/html
    try:
        msg.send()
    except SMTPRecipientsRefused as e:
        logger.error(str(e))
