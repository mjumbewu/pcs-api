import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.renderers.html.login import LoginHtmlView
from pcs.renderers.html.session import SessionHtmlView
from pcs.source.screenscrape.session import SessionScreenscrapeSource

class LoginHandler (webapp.RequestHandler):
    """
    Handles requests for a mechanism to login
    """
    def __init__(self, login_view):
        super(LoginHandler, self).__init__()
        self.login_view = login_view
    
    def get_user(self):
        username = self.request.get('username')
        return username
    
    def get(self):
        username = self.get_user()
        
        response_body = self.login_view.get_login_form(username)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()

class LoginHtmlHandler (LoginHandler):
    def __init__(self):
        super(LoginHtmlHandler, self).__init__(LoginHtmlView())

class CookiesHandler (webapp.RequestHandler):
    def get(self):
        from pcs.data.session import Session
        session = Session.FromRequest(self.request)
        
        self.response.out.write('<html><textarea>')
        self.response.out.write('sid='+session.id)
        self.response.out.write('</textarea></html>')


application = webapp.WSGIApplication(
        [('/login.html', LoginHtmlHandler),
         ('/cookies', CookiesHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
