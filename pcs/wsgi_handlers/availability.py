from pcs.wsgi_handlers.base import _SessionBasedHandler
from pcs.wsgi_handlers.base import _TimeRangeBasedHandler
from pcs.wsgi_handlers.base import WsgiParameterError
from pcs.fetchers.screenscrape.session import SessionScreenscrapeSource
from pcs.fetchers.screenscrape.availability import AvailabilityScreenscrapeSource
from pcs.fetchers.screenscrape.locations import LocationsScreenscrapeSource
from pcs.renderers.json.availability import AvailabilityJsonView
from pcs.renderers.json.error import ErrorJsonView
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
        vehicles = self.vehicle_source.fetch_available_vehicles_near(sessionid, locationid, start_time, end_time)
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
        if locationid and ',' in locationid:
            comma = locationid.find(',')
            lat = locationid[:comma]
            lon = locationid[comma+1:]
            location = self.location_source.fetch_custom_location('My Current Location', (lat, lon))
        else:
            location = self.location_source.fetch_location_profile(sessionid, locationid)
        
        return location
    
    
    
    def get(self, locationid):
        try:
            sessionid = self.get_session_id()
            
            if locationid == '_form':
                locationid = self.get_location_id()
            elif locationid == '_default':
                locationid = None
            
            location = self.get_location(sessionid, locationid)
            
            start_time, end_time = self.get_time_range()

            vehicle_availabilities = self.get_available_vehicles(sessionid, location.id, start_time, end_time)
            
            response_body = self.vehicle_view.render_location_availability(
                None, location, start_time, end_time, vehicle_availabilities)
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
    
    def get(self, vehicleid):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            session = self.get_session(userid, sessionid)
            start_time, end_time = self.get_time_range()
            
            vehicle_availability = self.vehicle_source.fetch_vehicle_availability(sessionid, vehicleid, start_time, end_time)
            price = self.vehicle_source.fetch_vehicle_price_estimate(sessionid, vehicleid, start_time, end_time)
            
            vehicle_availability.price = price
            
            response_body = self.vehicle_view.render_vehicle_availability(
                session, vehicle_availability)
        
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200);

class LocationAvailabilityJsonHandler (LocationAvailabilityHandler):
    def __init__(self):
        super(LocationAvailabilityJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            AvailabilityScreenscrapeSource(),
            LocationsScreenscrapeSource(),
            AvailabilityJsonView(),
            ErrorJsonView())
    
class VehicleAvailabilityJsonHandler (VehicleAvailabilityHandler):
    def __init__(self):
        super(VehicleAvailabilityJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            AvailabilityScreenscrapeSource(),
            AvailabilityJsonView(),
            ErrorJsonView())
    

