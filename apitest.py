import webapp2
import sys
sys.path.append('lib/requests')
sys.path.append('lib/gspread')

import requests
import config_manager

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(repr(
            config_manager.get_config('OPERATIONAL Job Fetch Bots')))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
