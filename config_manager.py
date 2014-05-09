import patch_httplib
import gspread
import json
import logging
import os

from google.appengine.api.app_identity import get_application_id
from google.appengine.api import memcache

appname = get_application_id()
session = None
CACHE_TIME = 20

def read_sheet(name=None, key=None):
    global session
    if not session:
        session = gspread.login(secrets['mail'], secrets['pass'])

    if name is not None:
        sheet = session.open(name).sheet1
    else:
        sheet = session.open_by_key(key).sheet1
    cell_values = sheet.get_all_values()
    headers = cell_values[0]
    items = cell_values[2:]
    configs = [ dict(zip(headers, item)) for item in items ]
    logging.info('configs %s', configs)
    for config in configs:
        if config['appid'] == appname:
            return config
    raise ValueError('no config for %s' % appname)

def get_config(name=None, key=None):
    mcache_key = 'config-%s-%s' % (name, key)
    conf = memcache.get(mcache_key)
    if not conf:
        conf = read_sheet(name=name, key=key)
        conf = json.dumps(conf)
        memcache.set(mcache_key, conf, CACHE_TIME)

    return json.loads(conf)

dir = os.path.dirname(__file__)
secret_path = 'secret.json'

secrets = eval(open(secret_path).read())
