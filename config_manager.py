import patch_httplib
import gspread
import json
import logging
import os

from google.appengine.api.app_identity import get_application_id
from google.appengine.api import memcache

appname = get_application_id()
session = None
CACHE_TIME = 3600 * 10

def read_sheet_raw(name=None, key=None):
    global session
    if not session:
        session = gspread.login(secrets['mail'], secrets['pass'])

    if name is not None:
        sheet = session.open(name).sheet1
    else:
        sheet = session.open_by_key(key).sheet1
    cell_values = sheet.get_all_values()
    return cell_values

def read_sheet(name, can_cache=True):
    mcache_key = 'sheet-%s' % name
    conf = memcache.get(mcache_key)
    if not (conf and can_cache):
        conf = read_sheet_raw(name)
        conf = json.dumps(conf)
        memcache.set(mcache_key, conf, CACHE_TIME)

    return json.loads(conf)

def get_config(name, can_cache=True):
    cell_values = read_sheet(name, can_cache=can_cache)
    headers = cell_values[0]
    items = cell_values[2:]
    configs = [ dict(zip(headers, item)) for item in items ]

    for config in configs:
        if config['appid'] == appname:
            return config
    raise ValueError('no config for %s' % appname)

dir = os.path.dirname(__file__)
secret_path = 'secret.json'

secrets = eval(open(secret_path).read())
