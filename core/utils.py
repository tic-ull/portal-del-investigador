# -*- encoding: UTF-8 -*-

from django.conf import settings as st
import json
import redis
import urllib

POOL = redis.ConnectionPool(host=st.REDIS_HOST, port=st.REDIS_PORT,
                            db=st.REDIS_DB, password=st.REDIS_PASSWORD)


def get_redis(key):
    r = redis.Redis(connection_pool=POOL)
    return r.get(key)


def set_redis(key, value):
    r = redis.Redis(connection_pool=POOL)
    r.set(key, value)


def wsget(ws):
    try:
        ws_json = json.loads(urllib.urlopen(ws).read())
        if (type(ws_json) is dict and
                'faultcode' in ws_json.keys()):
            return get_redis(ws)
        set_redis(ws, ws_json)
        return ws_json
    except:
        return get_redis(ws)
