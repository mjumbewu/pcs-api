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
from pcs.source.screenscrape.vehicles import VehiclesScreenscrapeSource
from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
from pcs.view.html.vehicles import VehiclesHtmlView
from pcs.view.html.error import ErrorHtmlView

class VehiclesHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    """
    Handles requests vehicle information
    """
    def __init__(self,
                 session_source,
                 vehicle_source,
                 location_source,
                 vehicle_view,
                 error_view):
        super(VehiclesHandler, self).__init__(session_source, error_view)
        
        self.vehicle_source = vehicle_source
        self.location_source = location_source
        self.vehicle_view = vehicle_view
    
    def get_available_vehicles(self, start_time, end_time):
        sessionid = self.get_session_id()
        locationid = self.get_location_id()
        
        return self.vehicle_source.get_available_vehicles_near(sessionid, locationid, start_time, end_time)
    
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
            
            response_body = self.vehicle_view.get_vehicle_availability(
                session, start_time, end_time, vehicles, location)
        except Exception, e:
            response_body = self.generate_error(e)
            
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()

class VehicleHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    def __init__(self, session_source, vehicle_source, 
                 vehicle_view, error_view):
        super(VehicleHandler, self).__init__(session_source, error_view)
        
        self.vehicle_source = vehicle_source
        self.vehicle_view = vehicle_view
    
    def save_vehicle_id(self, vehicleid):
        self.vehicleid = vehicleid
    
    def get_vehicle_id(self):
        try:
            return self.vehicleid
        except AttributeError:
            raise WsgiParameterError('Vehicle id must be specified')
    
    def get_vehicle(self):
        sessionid = self.get_session_id()
        vehicleid = self.get_vehicle_id()
        vehicle = self.vehicle_source.get_vehicle(sessionid, vehicleid)
        return vehicle
    
    def get_availability(self):
        sessionid = self.get_session_id()
        vehicleid = self.get_vehicle_id()
        start_time, end_time = self.get_time_range()
        availability = self.vehicle_source.get_vehicle_availability(sessionid, vehicleid, start_time, end_time)
        return availability
    
    def get(self, vehicleid):
        self.save_vehicle_id(vehicleid)
        
        session = self.get_session()
        vehicle = self.get_vehicle()
        start_time, end_time = self.get_time_range()
        availability = self.get_availability()
        price = self.get_price_estimate()
        
        response_body = self.vehicle_view.get_vehicle(session, vehicle,
            start_time, end_time, availability, price)
        
        self.response.out.write(response_body);
        self.response.set_status(200);

class VehiclesHtmlHandler (VehiclesHandler):
    def __init__(self):
        super(VehiclesHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            VehiclesScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            VehiclesHtmlView(),
            ErrorHtmlView())
    
class VehicleHtmlHandler (VehicleHandler):
    def __init__(self):
        super(VehicleHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            VehiclesScreenscrapeSource(),
            VehiclesHtmlView(),
            ErrorHtmlView())

application = webapp.WSGIApplication(
        [('/vehicles.html', VehiclesHtmlHandler),
         ('/vehicles/(.*).html', VehicleHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
