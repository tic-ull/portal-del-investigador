# -*- encoding: UTF-8 -*-

from django.conf import settings as st


def _get_langs_info(languages, current_url):
    # Remove possible lang prefixes from current url
    base_url = current_url
    for language in languages:
        base_url = base_url.replace('/' + language[0] + '/', '/')

    # Create a list of available languages for the templates to use
    language_urls = []
    for language in languages:
        line = {'code': language[0], 'name': language[1],
                'url': '/' + language[0] + base_url}
        language_urls.append(line)
    return language_urls


def extra_info(request):
    return {
        'old_portal': st.OLD_PORTAL_URL,
        'cp_languages': _get_langs_info(st.LANGUAGES, request.path),
    }
