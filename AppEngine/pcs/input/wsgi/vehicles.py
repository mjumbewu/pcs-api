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
    
    def get_available_vehicles(self, sessionid, locationid, start_time, end_time):
        vehicles = self.vehicle_source.get_available_vehicles_near(sessionid, locationid, start_time, end_time)
        return vehicles
    
    def get_location_id(self):
        locationid = self.request.get('location_id')
        if locationid:
            return locationid
        
        latitude = self.request.get('latitude')
        longitude = self.request.get('longitude')
        if latitude and longitude:
            return (float(latitude), float(longitude))
        
        raise WsgiParameterError('No valid location given')
    
    def get_location(self, sessionid, locationid):
        if isinstance(locationid, (basestring, int)):
            location = self.location_source.get_location_profile(sessionid, locationid)
        else:
            location = self.location_source.get_custom_location('My Current Location', locationid)
        
        return location
    
    
    
    def get(self):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            locationid = self.get_location_id()
            
            session = self.get_session(userid, sessionid)
            location = self.get_location(sessionid, locationid)
            
            start_time, end_time = self.get_time_range()

            vehicles = self.get_available_vehicles(sessionid, locationid, start_time, end_time)
            
            response_body = self.vehicle_view.get_vehicle_availability(
                session, location, start_time, end_time, vehicles)
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
    
#    def get_vehicle_id(self):
#        vehicle_id = self.request.get('vehicle_id')
#        if vehicle_id is None:
#            raise WsgiParameterError('No vehicle id found')
#        return vehicle_id
#    
    def get_vehicle(self, sessionid, vehicleid, start_time, end_time):
        vehicle = self.vehicle_source.get_vehicle(sessionid, vehicleid, start_time, end_time)
        return vehicle
    
    def get_price_estimate(self, sessionid, vehicleid, start_time, end_time):
        price = self.vehicle_source.get_vehicle_price_estimate(sessionid, vehicleid, start_time, end_time)
        return price
    
    def get(self, vehicleid):
        userid = self.get_user_id()
        sessionid = self.get_session_id()
        session = self.get_session(userid, sessionid)
        start_time, end_time = self.get_time_range()
#        vehicleid = self.get_vehicle_id()
        
        vehicle = self.get_vehicle(sessionid, vehicleid, start_time, end_time)
        price = self.get_price_estimate(sessionid, vehicleid, start_time, end_time)
        
        response_body = self.vehicle_view.get_vehicle_info(session, vehicle,
            start_time, end_time, price)
        
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
        [('/availability.html', VehiclesHtmlHandler),
         ('/availability/(.*).html', VehicleHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
