import datetime
import os

from google.appengine.ext.webapp import template

class AvailabilityHtmlView (object):
    @staticmethod
    def get_vehicle_availability(session, start_time, end_time, vehicles, location):
        """
        Return a response with overview information about the given session.
        """
        values = {
            'session': session,
            'vehicles': vehicles,
            'location': location,
            'start_time': start_time,
            'end_time': end_time
        }
        
        path = os.path.join(os.path.dirname(__file__), 'available_cars.html')
        response = template.render(path, values)
        return response
    
