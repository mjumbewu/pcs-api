from pcs.wsgi_handlers.base import _SessionBasedHandler
from pcs.wsgi_handlers.base import WsgiParameterError
from pcs.fetchers.screenscrape.session import SessionScreenscrapeSource
from pcs.fetchers.screenscrape.locations import LocationsScreenscrapeSource
from pcs.renderers.json.error import ErrorJsonView
from pcs.renderers.json.locations import LocationsJsonView

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
            locations = self.locations_source.fetch_location_profiles(sessionid)
            response_body = self.locations_view.render_locations(session, locations)
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);

class LocationsJsonHandler (LocationsHandler):
    def __init__(self):
        super(LocationsJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            LocationsJsonView(),
            ErrorJsonView())
    

