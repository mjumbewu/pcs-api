import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.input.wsgi import _SessionBasedHandler
from pcs.view.html.error import ErrorHtmlView
from pcs.view.html.login import LoginHtmlView
from pcs.view.html.session import SessionHtmlView
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from util.abstract import override

class SessionHandler (_SessionBasedHandler):
    """
    Handles requests sent to the list of products
    """
    def __init__(self,
                 session_source,
                 session_view,
                 error_view):
        super(SessionHandler, self).__init__(session_source, error_view)
        
        self.session_view = session_view
    
    def get_credentials(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        return username, password
    
    @override
    def get_session(self):
        """
        Attempt to get a session using username and password credentials. If no
        password is available, attempt to find an existing session id to use.
        @return: A valid session or None
        """
        username, password = self.get_credentials()
        
        if username and password:
            session = self.session_source.get_new_session(username, password)
        else:
            session = super(SessionHandler, self).get_session()
        
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
        self.post()
    
    def post(self):
        try:
            session = self.get_session()
            
            response_body = self.session_view.get_session_overview(session)
            if session: self.save_session(session)
        
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
        
        # Put the original body in a comment.
#        pcs_login_body = self.session_source._body
#        pcs_login_body.replace('-->', 'end_comment')
#        self.response.out.write('<!-- %s -->' % pcs_login_body)

class SessionHtmlHandler (SessionHandler):
    def __init__(self):
        super(SessionHtmlHandler, self).__init__(SessionScreenscrapeSource(), 
                                                 SessionHtmlView(),
                                                 ErrorHtmlView())



application = webapp.WSGIApplication(
        [('/session.html', SessionHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
