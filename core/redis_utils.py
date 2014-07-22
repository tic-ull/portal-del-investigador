# -*- encoding: UTF-8 -*-

from django.conf import settings as st
import json
import redis
import urllib

POOL = redis.ConnectionPool(host=st.REDIS_HOST, port=st.REDIS_PORT,
                            db=st.REDIS_DB, password=st.REDIS_PASSWORD)


def wsget(ws, use_redis=True, timeout=st.REDIS_TIMEOUT):
    try:
        ws_json = json.loads(urllib.urlopen(ws).read())
        if (type(ws_json) is dict and
                'faultcode' in ws_json.keys()):
            return get_from_redis_or_none(ws, use_redis)
        if use_redis:
            set_redis(ws, timeout, ws_json)
        return ws_json
    except:
        return get_from_redis_or_none(ws, use_redis)


def get_from_redis_or_none(ws, use_redis):
    if use_redis:
        return eval_get_redis(ws)
    return None


def eval_get_redis(ws):
    value = get_redis(ws)
    if value is not None:
        return eval(value.decode('string-escape'))
    return None


def get_redis(key):
    try:
        r = redis.Redis(connection_pool=POOL)
        return r.get(key)
    except redis.ConnectionError:
        return None


def set_redis(key, timeout, value):
    try:
        r = redis.Redis(connection_pool=POOL)
        r.set(key, value)
        if timeout is not None and str(timeout).isdigit():
            r.expire(key, timeout)
    except redis.ConnectionError:
        pass
