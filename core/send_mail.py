# -*- encoding: UTF-8 -*-

from django.conf import settings as st
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from smtplib import SMTPRecipientsRefused
import logging

logger = logging.getLogger('default')

def send_mail_from_template(subject='', template='', context='', email_to=''):
    try:
        body = render_to_string(template, context)
        msg = EmailMessage(subject, body, st.EMAIL_HOST_USER, [email_to])
        msg.content_subtype = "html"
        msg.send()
    except SMTPRecipientsRefused as e:
        logger.error('Error en el envío: ' + str(e))