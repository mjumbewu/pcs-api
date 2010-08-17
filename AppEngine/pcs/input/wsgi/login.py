import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.view.html.login import LoginHtmlView
from pcs.view.html.session import SessionHtmlView
from pcs.source.screenscrape.login import LoginScreenscrapeSource

class LoginHandler (webapp.RequestHandler):
    """
    Handles requests sent to the list of products
    """
    def __init__(self):
        super(LoginHandler, self).__init__()
    
    def get_user(self):
        username = self.request.get('username')
        return username
    
    def get(self):
        username = self.get_user()
        
        view = LoginHtmlView()
        response_body = view.show_login_form(username)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()

class CookiesHandler (webapp.RequestHandler):
    def get(self):
        session = Session.FromRequest(self.request)
        
        self.response.out.write('<html><textarea>')
        self.response.out.write('sid='+session.id)
        self.response.out.write('</textarea></html>')


application = webapp.WSGIApplication(
        [('/login', LoginHandler),
         ('/cookies', CookiesHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
