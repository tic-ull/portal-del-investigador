# -*- encoding: UTF-8 -*-

from crequest.middleware import CrequestMiddleware
from core.models import UserProfile
from django.conf import settings as st
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import simplejson as json
import urllib


def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    profile = UserProfile.objects.create(user=instance)
    request = CrequestMiddleware.get_request()
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
        if 'NumDocumento' in cas_info:
            profile.documento = cas_info['NumDocumento']
            WS = st.WS_SERVER_URL + 'get_codpersona?nif=%s' % (
                cas_info['NumDocumento'])
            if urllib.urlopen(WS).code == 200:
                profile.rrhh_code = json.loads(urllib.urlopen(WS).read())
    profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="create-profile")
