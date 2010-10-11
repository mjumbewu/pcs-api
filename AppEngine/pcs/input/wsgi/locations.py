import httplib
import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.input.wsgi import _SessionBasedHandler
from pcs.input.wsgi import WsgiParameterError
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
from pcs.view.html.error import ErrorHtmlView
from pcs.view.html.locations import LocationsHtmlView
from pcs.view.json.error import ErrorJsonView
from pcs.view.json.locations import LocationsJsonView

class LocationsHandler (_SessionBasedHandler):
    """
    Handles requests availability information
    """
    def __init__(self,
                 session_source,
                 locations_source,
                 locations_view,
                 error_view):
        super(LocationsHandler, self).__init__(session_source, error_view)
        
        self.locations_source = locations_source
        self.locations_view = locations_view
    
    def get(self):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            
            session = self.get_session(userid, sessionid)
            locations = self.locations_source.get_location_profiles(sessionid)
            response_body = self.locations_view.render_locations(session, locations)
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);

class LocationsHtmlHandler (LocationsHandler):
    def __init__(self):
        super(LocationsHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            LocationsHtmlView(),
            ErrorHtmlView())

class LocationsJsonHandler (LocationsHandler):
    def __init__(self):
        super(LocationsJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            LocationsJsonView(),
            ErrorJsonView())
    


application = webapp.WSGIApplication(
        [('/locations.html', LocationsHtmlHandler),
         ('/locations.json', LocationsJsonHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
