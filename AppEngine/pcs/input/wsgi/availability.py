import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.input.wsgi import WsgiParameterError
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
from pcs.view.html.availability import AvailabilityHtmlView
from util.TimeZone import Eastern

class AvailabilityHandler (webapp.RequestHandler):
    """
    Handles requests availability information
    """
    def __init__(self,
                 session_source,
                 availability_source,
                 location_source,
                 availability_view):
        super(AvailabilityHandler, self).__init__()
        
        self.session_source = session_source
        self.availability_source = availability_source
        self.location_source = location_source
        self.availability_view = availability_view
    
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
        username, session_id = self.get_session_id()
        session = self.session_source.get_existing_session(username, session_id)
        
        return session
    
    def get_available_vehicles(self, sessionid, locationid, start_time, end_time):
        return self.availability_source.get_available_vehicles_near(sessionid, locationid, start_time, end_time)
    
    def get_location_id(self):
        locationid = self.request.get('location_id')
        if locationid is not None:
            return locationid
        
        latitude = self.request.get('latitude')
        longitude = self.request.get('longitude')
        if latitude is not None and longitude is not None:
            return (latitude, longitude)
        
        raise WsgiParameterError('No valid location given')
    
    def get_location(self, sessionid, locationid):
        if isinstance(locationid, (basestring, int)):
            location = self.location_source.get_location_profile(sessionid, locationid)
        else:
            location = self.location_source.get_custom_location('My Current Location', locationid)
        
        return location
    
    def get_time_range(self):
        import datetime
        start_time_str = self.request.get('start_time')
        end_time_str = self.request.get('end_time')
        
        now_time = datetime.datetime.now(Eastern) + datetime.timedelta(minutes=15)
        if start_time_str:
            start_time = datetime.datetime.fromtimestamp(int(start_time_str))
        else:
            start_time = now_time
        
        if end_time_str:
            end_time = datetime.datetime.fromtimestamp(int(end_time_str))
        else:
            end_time = now_time + datetime.timedelta(hours=3)
        
        return start_time, end_time
        
        
    def get(self):
        session = self.get_session()
        start_time, end_time = self.get_time_range()
        locationid = self.get_location_id()
        
        sessionid = session.id if session is not None else 0
        location = self.get_location(sessionid, locationid)
        
        vehicles = self.get_available_vehicles(sessionid, locationid, start_time, end_time) if session else []
        
        response_body = self.availability_view.get_vehicle_availability(
            session, start_time, end_time, vehicles, location)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()

class AvailabilityHtmlHandler (AvailabilityHandler):
    def __init__(self):
        super(AvailabilityHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            AvailabilityScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            AvailabilityHtmlView())
    


application = webapp.WSGIApplication(
        [('/availability.html', AvailabilityHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
