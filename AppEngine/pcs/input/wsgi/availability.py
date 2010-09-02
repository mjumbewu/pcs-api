import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.input.wsgi import _SessionBasedHandler
from pcs.input.wsgi import _TimeRangeBasedHandler
from pcs.input.wsgi import WsgiParameterError
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
from pcs.view.html.availability import AvailabilityHtmlView
from pcs.view.html.error import ErrorHtmlView

class AvailabilityHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    """
    Handles requests availability information
    """
    def __init__(self,
                 session_source,
                 availability_source,
                 location_source,
                 availability_view,
                 error_view):
        super(AvailabilityHandler, self).__init__(session_source, error_view)
        
        self.availability_source = availability_source
        self.location_source = location_source
        self.availability_view = availability_view
    
    def get_available_vehicles(self, start_time, end_time):
        sessionid = self.get_session_id()
        locationid = self.get_location_id()
        
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
    
    def get_location(self):
        sessionid = self.get_session_id()
        locationid = self.get_location_id()
        
        if isinstance(locationid, (basestring, int)):
            location = self.location_source.get_location_profile(sessionid, locationid)
        else:
            location = self.location_source.get_custom_location('My Current Location', locationid)
        
        return location
    
    def get(self):
        try:
            session = self.get_session()
            location = self.get_location()
            start_time, end_time = self.get_time_range()

            vehicles = self.get_available_vehicles(start_time, end_time)
            
            response_body = self.availability_view.get_vehicle_availability(
                session, start_time, end_time, vehicles, location)
        except Exception, e:
            response_body = self.generate_error(e)
            
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
            AvailabilityHtmlView(),
            ErrorHtmlView())
    


application = webapp.WSGIApplication(
        [('/availability.html', AvailabilityHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
