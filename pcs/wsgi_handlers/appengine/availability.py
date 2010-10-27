import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.wsgi_handlers.appengine import _SessionBasedHandler
from pcs.wsgi_handlers.appengine import _TimeRangeBasedHandler
from pcs.wsgi_handlers.appengine import WsgiParameterError
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
from pcs.view.html.availability import AvailabilityHtmlView
from pcs.view.html.error import ErrorHtmlView
from pcs.view.json.availability import AvailabilityJsonView
from pcs.view.json.error import ErrorJsonView
from util.abstract import override
from util.TimeZone import Eastern

class LocationAvailabilityHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    """
    Handles requests vehicle information
    """
    def __init__(self,
                 session_source,
                 vehicle_source,
                 location_source,
                 vehicle_view,
                 error_view):
        super(LocationAvailabilityHandler, self).__init__(session_source, error_view)
        
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
        if locationid is None or isinstance(locationid, (basestring, int)):
            location = self.location_source.get_location_profile(sessionid, locationid)
        else:
            location = self.location_source.get_custom_location('My Current Location', locationid)
        
        return location
    
    
    
    def get(self, locationid):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            
            if locationid == '.form':
                locationid = self.get_location_id()
            elif locationid == '.default':
                locationid = None
            
            session = self.get_session(userid, sessionid)
            location = self.get_location(sessionid, locationid)
            
            start_time, end_time = self.get_time_range()

            vehicle_availabilities = self.get_available_vehicles(session.id, location.id, start_time, end_time)
            
            response_body = self.vehicle_view.render_location_availability(
                session, location, start_time, end_time, vehicle_availabilities)
        except Exception, e:
            response_body = self.generate_error(e)
            
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()

class VehicleAvailabilityHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    def __init__(self, session_source, vehicle_source, 
                 vehicle_view, error_view):
        super(VehicleAvailabilityHandler, self).__init__(session_source, error_view)
        
        self.vehicle_source = vehicle_source
        self.vehicle_view = vehicle_view
    
    def get_vehicle(self, sessionid, vehicleid, start_time, end_time):
        vehicle = self.vehicle_source.get_vehicle(sessionid, vehicleid, start_time, end_time)
        return vehicle
    
    def get_price_estimate(self, sessionid, vehicleid, start_time, end_time):
        price = self.vehicle_source.get_vehicle_price_estimate(sessionid, vehicleid, start_time, end_time)
        return price
    
    def get_updated_transaction(self, sessionid, vehicleid, start_time, end_time):
        transaction = self.vehicle_source.get_updated_transaction(sessionid, vehicleid, start_time, end_time)
        return transaction
    
    def get(self, vehicleid):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            session = self.get_session(userid, sessionid)
            start_time, end_time = self.get_time_range()
            
            vehicle = self.get_vehicle(sessionid, vehicleid, start_time, end_time)
            price = self.get_price_estimate(sessionid, vehicleid, start_time, end_time)
#            transaction = self.get_updated_transaction(sessionid, vehicleid, start_time, end_time)
            
#            session.transaction = transaction
            
            response_body = self.vehicle_view.render_vehicle_availability(session, vehicle,
                start_time, end_time, price)
        
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);

class LocationAvailabilityHtmlHandler (LocationAvailabilityHandler):
    def __init__(self):
        super(LocationAvailabilityHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            AvailabilityScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            AvailabilityHtmlView(),
            ErrorHtmlView())
    
    @override
    def get_time_range(self):
        return self.get_separate_iso_date_and_time_range()
    
class LocationAvailabilityJsonHandler (LocationAvailabilityHandler):
    def __init__(self):
        super(LocationAvailabilityJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            AvailabilityScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            AvailabilityJsonView(),
            ErrorJsonView())
    
class VehicleAvailabilityHtmlHandler (VehicleAvailabilityHandler):
    def __init__(self):
        super(VehicleAvailabilityHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            AvailabilityScreenscrapeSource(),
            AvailabilityHtmlView(),
            ErrorHtmlView())

application = webapp.WSGIApplication(
        [('/locations/(.*)/availability.html', LocationAvailabilityHtmlHandler),
         ('/locations/(.*)/availability.json', LocationAvailabilityJsonHandler),
         ('/vehicles/(.*)/availability.html', VehicleAvailabilityHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
