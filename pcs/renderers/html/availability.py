import datetime
import os

from google.appengine.ext.webapp import template

from pcs.renderers import _AvailabilityViewInterface
from util.abstract import override
from util.TimeZone import to_xchange_time

class AvailabilityHtmlView (_AvailabilityViewInterface):
    def __init__(self, render_method=template.render):
        self.render_method = render_method
    
    @override
    def render_location_availability(self, session, location, start_time, end_time, vehicle_availabilities):
        """
        Return a response with vehicle availability near a given location
        """
        values = {
            'session': session,
            'vehicle_availabilities': vehicle_availabilities,
            'location': location,
            'start_time': start_time,
            'end_time': end_time,
            'start_stamp': to_xchange_time(start_time),
            'end_stamp': to_xchange_time(end_time)
        }
        
        path = os.path.join(os.path.dirname(__file__), 'available_cars.html')
        response = self.render_method(path, values)
        return response
    
    @override
    def render_vehicle_availability(self, session, vehicle, start_time, end_time, price):
        """
        Return a response with the availability of the given vehicle
        """
        values = {
            'session': session,
            'vehicle': vehicle,
            'start_time': start_time,
            'end_time': end_time,
            'price': price,
            'start_stamp': to_xchange_time(start_time),
            'end_stamp': to_xchange_time(end_time)
        }
        
        path = os.path.join(os.path.dirname(__file__), 'vehicle_info.html')
        response = self.render_method(path, values)
        return response
