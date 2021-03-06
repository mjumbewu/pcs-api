import datetime
import os

from google.appengine.ext.webapp import template

from pcs.renderers import _AvailabilityViewInterface
from util.abstract import override
from util.TimeZone import to_xchange_time

class AvailabilityJsonView (_AvailabilityViewInterface):
    def __init__(self, render_method=template.render):
        self.render_method = render_method
    
    @override
    def render_location_availability(self, session, location, start_time, end_time, vehicle_availabilities):
        """
        Return a response with vehicle availability near a given location
        """
        class LocationCopy (object):
            def __init__(self, location):
                self.name = location.name
                if isinstance(location.id, tuple):
                    self.id = '%s,%s' % location.id
                else:
                    self.id = location.id
        
        values = {
            'session': session,
            'location': location if isinstance(location, str) else LocationCopy(location),
            'start_time': start_time,
            'end_time': end_time,
            'start_stamp': to_xchange_time(start_time),
            'end_stamp': to_xchange_time(end_time),
            'vehicle_availabilities': vehicle_availabilities
        }
        
        path = os.path.join(os.path.dirname(__file__), 'location_availability.json')
        response = self.render_method(path, values)
        return response
    
    @override
    def render_vehicle_availability(self, session, vehicle_availability):
        """
        Return a response with the availability of the given vehicle
        """
        values = {
            'session': session,
            'vehicle': vehicle_availability.vehicle,
            'start_time': vehicle_availability.start_time,
            'end_time': vehicle_availability.end_time,
            'price': vehicle_availability.price
        }
        
        path = os.path.join(os.path.dirname(__file__), 'vehicle_availability.json')
        response = self.render_method(path, values)
        return response
