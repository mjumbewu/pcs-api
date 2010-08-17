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
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/my_reservations.php"):
        super(LoginHandler, self).__init__()
        self.__host = host
        self.__path = path
    
    def get_credentials(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        return username, password
    
    def get_session_id(self):
        username = self.request.cookies.get('suser', None)
        session_id = self.request.cookies.get('sid', None)
        
        return username, session_id
    
    def get_session(self):
        """
        Attempt to get a session using username and password credentials. If no
        password is available, attempt to find an existing session id to use.
        @return: A valid session or None
        """
        username, password = self.get_credentials()
        
        if username and password:
            source = LoginScreenscrapeSource()
            session = source.get_new_session(username, password)
        else:
            username, session_id = self.get_session_id()
            source = LoginScreenscrapeSource()
            session = source.get_existing_session(username, session_id)
        
        return session
    
    def save_session(self, session):
        """
        Attempt to save the given login session to a cookie on the user's 
        machine.
        """
        self.response.headers.add_header('Set-Cookie',str('sid='+session.id+'; path=/'))
        self.response.headers.add_header('Set-Cookie',str('suser='+session.user+'; path=/'))
        self.response.headers.add_header('Set-Cookie',str('sname='+session.name+'; path=/'))
        
    def get(self):
#        session = self.get_session()
        username, password = self.get_credentials()
        
        if username and password:
            source = LoginScreenscrapeSource()
            session = source.get_new_session(username, password)
        else:
            username, session_id = self.get_session_id()
            source = LoginScreenscrapeSource()
            session = source.get_existing_session(username, session_id)
        
        if session:
            view = SessionHtmlView()
            response_body = view.get_session_overview(session)
            self.save_session(session)
        else:
            view = LoginHtmlView()
            response_body = view.get_login_form()
        
        self.response.out.write(response_body);
        self.response.set_status(200);
        
        # Put the original body in a comment.
        pcs_login_body = source._body
        pcs_login_body.replace('-->', 'end_comment')
        self.response.out.write('<!-- %s -->' % pcs_login_body)
    
    def post(self):
        self.get()



application = webapp.WSGIApplication(
        [('/session', LoginHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
