import httplib
import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.input.wsgi import WsgiParameterError
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
from pcs.view.html.locations import LocationsHtmlView

class LocationsHandler (webapp.RequestHandler):
    """
    Handles requests availability information
    """
    def __init__(self,
                 session_source,
                 locations_source,
                 locations_view):
        super(LocationsHandler, self).__init__()
        
        self.session_source = session_source
        self.locations_source = locations_source
        self.locations_view = locations_view
    
    def get_session_id(self):
        username = self.request.cookies.get('suser', None)
        session_id = self.request.cookies.get('sid', None)
        
        if username is None: raise WsgiParameterError('Missing Required Cookie', 'suser')
        if session_id is None: raise WsgiParameterError('Missing Required Cookie', 'sid')
        
        return username, session_id
    
    def get_session(self):
        """
        Attempt to get a session using username and password credentials. If no
        password is available, attempt to find an existing session id to use.
        @return: A valid session or None
        """
        username, session_id = self.get_session_id()
        session = self.session_source.get_existing_session(username, session_id)
        
        return session
    
    def generate_error(self, exception):
        from pcs.view.html.error import ErrorHtmlView
        error_view = ErrorHtmlView()
        
        return error_view.get_error(None, type(exception).__name__ + ': ' + str(exception))
    
    def get(self):
        try:
            session = self.get_session()
            locations = self.locations_source.get_location_profiles(session.id)
            response_body = self.locations_view.get_locations(session, locations)
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()

class LocationsHtmlHandler (LocationsHandler):
    def __init__(self):
        super(LocationsHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            LocationsHtmlView())
    


application = webapp.WSGIApplication(
        [('/locations.html', LocationsHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
