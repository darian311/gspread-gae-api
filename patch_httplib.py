import httplib
import requests.packages.urllib3.connection

requests.packages.urllib3.connection.HTTPSConnection._protocol = 'https'
