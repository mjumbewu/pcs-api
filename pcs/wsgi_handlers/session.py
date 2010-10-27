import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.wsgi_handlers.base import _SessionBasedHandler
from pcs.wsgi_handlers.base import WsgiParameterError
from pcs.renderers.html.error import ErrorHtmlView
from pcs.renderers.html.login import LoginHtmlView
from pcs.renderers.html.session import SessionHtmlView
from pcs.renderers.json.error import ErrorJsonView
from pcs.renderers.json.session import SessionJsonView
from pcs.fetchers.screenscrape.session import SessionScreenscrapeSource
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
        username = self.request.get('user')
        password = self.request.get('password')
        
        if username in ('', None) or password in ('', None):
            raise WsgiParameterError('Both userid and password must be supplied')
        
        return username, password
    
    def get_new_session(self, userid, password):
        """
        Attempt to get a session using username and password credentials. If no
        password is available, attempt to find an existing session id to use.
        @return: A valid session or None
        """
        session = self.session_source.get_new_session(userid, password)
        return session
    
    def save_session(self, session):
        """
        Attempt to save the given login session to a cookie on the user's 
        machine.
        """
        session_data = {
            'id':session.id,
            'user':session.user,
            'name':session.name
        }
        
        session_string = json.dumps(session_data).replace(r'"', r'\"')
        self.response.headers.add_header('Set-Cookie',str('session="'+session_string+'"; path=/'))
        
    def get(self):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            session = self.get_session(userid, sessionid)
            
            response_body = self.session_view.render_session(session)
        
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        try:
            userid, password = self.get_credentials()
            session = self.get_new_session(userid, password)
            
            response_body = self.session_view.render_session(session)
            self.save_session(session)
        
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);

class SessionHtmlHandler (SessionHandler):
    def __init__(self):
        super(SessionHtmlHandler, self).__init__(SessionScreenscrapeSource(), 
                                                 SessionHtmlView(),
                                                 ErrorHtmlView())

class SessionJsonHandler (SessionHandler):
    def __init__(self):
        super(SessionJsonHandler, self).__init__(SessionScreenscrapeSource(), 
                                                 SessionJsonView(),
                                                 ErrorJsonView())



application = webapp.WSGIApplication(
        [('/session.html', SessionHtmlHandler),
         ('/session.json', SessionJsonHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
