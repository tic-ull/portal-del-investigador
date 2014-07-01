# -*- encoding: UTF-8 -*-

import json
import urllib


def wsget(ws):
    try:
        ws_json = json.loads(urllib.urlopen(ws).read())
        if 'faultcode' in ws_json.keys():
            raise(IOError)
    except IOError:
        return None
    return ws_json
