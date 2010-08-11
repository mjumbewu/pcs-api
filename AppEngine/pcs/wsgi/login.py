import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.html.login import LoginHtmlView
from pcs.screenscrape.login import LoginScreenscrapeSource

class LoginHandler (webapp.RequestHandler):
    """
    Handles requests sent to the list of products
    """
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/my_reservations.php"):
        super(LoginHandler, self).__init__()
        self.__host = host
        self.__path = path
    
    def get_credentials(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        return username, password
    
    def save_session(self, session):
        """
        Attempt to save the given login session to a cookie on the user's 
        machine.
        """
        self.response.headers.add_header('Set-Cookie',str('sid='+session.id+'; path=/'))
        self.response.headers.add_header('Set-Cookie',str('suser='+session.user+'; path=/'))
        self.response.headers.add_header('Set-Cookie',str('sname='+session.name+'; path=/'))
        
    def get(self):
        username, password = self.get_credentials()
        
        source = LoginScreenscrapeSource()
        view = LoginHtmlView()
        
        session = source.get_new_session(username, password)
        if session:
            response_body = view.SuccessResponse(session)
            self.save_session(session)
        else:
            response_body = view.FailureResponse(username)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
        
        # Put the original body in a comment.
        pcs_login_body = source._body
        pcs_login_body.replace('-->', 'end_comment')
        self.response.out.write('<!-- %s -->' % pcs_login_body)
    
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
