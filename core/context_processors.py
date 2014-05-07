from django.conf import settings


def external_urls(request):
    urls = {'old_portal': settings.OLD_PORTAL_URL}
    return urls
