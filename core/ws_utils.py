# -*- encoding: UTF-8 -*-

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
        except:
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
