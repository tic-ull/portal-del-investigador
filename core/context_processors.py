# -*- encoding: UTF-8 -*-

#
#    Copyright 2014-2015
#
#      STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Portal del Investigador is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Portal del Investigador.  If not, see
#    <http://www.gnu.org/licenses/>.
#

from django.conf import settings as st
from crequest.middleware import CrequestMiddleware


def _get_langs_info(languages, current_url):
    """
    List of languages for the language picker
    """
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
    request = CrequestMiddleware.get_request()
    cas_info = None
    if request and 'attributes' in request.session:
        cas_info = request.session['attributes']
    # In some cases the user can be AnonymousUser, and doesnt have first_name
    # or last_name. This can happen if we want to show an error message to
    # a user that cant login
    try:
        first_name = (cas_info['first_name']
                      if cas_info and 'first_name' in cas_info
                      else request.user.first_name)
    except AttributeError:
        first_name = ''
    try:
        last_name = (cas_info['last_name']
                     if cas_info and 'last_name' in cas_info
                     else request.user.last_name)
    except AttributeError:
        last_name = ''
    return {
        'old_portal': st.OLD_PORTAL_URL,
        'cp_languages': _get_langs_info(st.LANGUAGES, request.path),
        'first_name': first_name,
        'last_name': last_name,
        'datatables_js_url': st.DATATABLES_JS_URL,
        'datatables_css_url': st.DATATABLES_CSS_URL,
        'datatables_order_plugin': st.DATATABLES_ORDER_PLUGIN_URL,
    }


def installed_apps(request):
    return {
        'is_accounting_installed': 'accounting' in st.INSTALLED_APPS,
        'is_statistics_installed': 'statistics' in st.INSTALLED_APPS,
    }
