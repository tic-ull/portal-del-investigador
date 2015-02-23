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
import json
import redis
import urllib
import logging

logger = logging.getLogger('default')


def eval_json(value):
    if value is not None:
        return eval(value.decode('string-escape'))
    return None


class CachedWS:

    r = redis.Redis(host=st.REDIS_HOST, port=st.REDIS_PORT,
                    db=st.REDIS_DB, password=st.REDIS_PASSWORD)

    def __new__(cls, *args, **kwargs):
        return cls

    @classmethod
    def get(cls, url, use_redis=True, timeout=st.REDIS_TIMEOUT):
        ws_json = None
        try:
            reply = json.loads(urllib.urlopen(url).read())
            if type(reply) is dict and 'faultcode' in reply:
                raise KeyError
            ws_json = reply
            if use_redis:
                cls._set_redis(url, timeout, ws_json)
        except (IOError, KeyError, ValueError):
            if use_redis:
                ws_json = eval_json(cls._get_redis(url))
                logger.error(u'No hay respuesta de ODIN para el WS'
                             u' %s - Se busca en REDIS' % url)
        return ws_json

    @classmethod
    def _get_redis(cls, key):
        try:
            return cls.r.get(key)
        except redis.ConnectionError:
            return None

    @classmethod
    def _set_redis(cls, key, timeout, value):
        try:
            cls.r.set(key, value)
            if timeout is not None and str(timeout).isdigit():
                cls.r.expire(key, timeout)
        except redis.ConnectionError:
            pass
