import patch_httplib
import gspread
import json
import logging

from google.appengine.api.app_identity import get_application_id
from google.appengine.api import memcache

appname = get_application_id()
session = None
CACHE_TIME = 20

def read_sheet(name):
    global session
    if not session:
        session = gspread.login(secrets['mail'], secrets['pass'])

    sheet = session.open(name).sheet1
    cell_values = sheet.get_all_values()
    headers = cell_values[0]
    items = cell_values[2:]
    configs = [ dict(zip(headers, item)) for item in items ]
    logging.info('configs %s', configs)
    for config in configs:
        if config['appid'] == appname:
            return config
    raise ValueError('no config for %s' % appname)

def get_config(name):
    conf = memcache.get('config')
    if not conf:
        conf = read_sheet(name)
        conf = json.dumps(conf)
        memcache.set('config', conf, CACHE_TIME)

    return json.loads(conf)

secrets = eval(open('secret.json').read())
