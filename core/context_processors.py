from django.conf import settings


def external_urls(request):
    return {'old_portal': settings.OLD_PORTAL_URL}
