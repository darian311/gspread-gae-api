import webapp2
import sys
sys.path.append('lib/requests')
sys.path.append('lib/gspread')

import patch_httplib
import gspread
secrets = eval(open('secret.json').read())

import requests

class MainPage(webapp2.RequestHandler):
    def get(self):
        gc = gspread.login(secrets['mail'], secrets['pass'])
        wks = gc.open('Foo').sheet1
        cell_list = wks.range('A1:B7')

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(repr(cell_list))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
