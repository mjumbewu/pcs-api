import datetime
import os

from google.appengine.ext.webapp import template

from pcs.renderers import _LocationsViewInterface
from util.abstract import override
from util.TimeZone import Eastern

class LocationsHtmlView (_LocationsViewInterface):
    def get_locations(self, session, locations):
        now_time = datetime.datetime.now(Eastern)
        minutes_past = now_time.minute % 15
        
        default_start = now_time + datetime.timedelta(minutes=(15-minutes_past))
        default_end = default_start + datetime.timedelta(hours=3)
        
        last_start = default_start + datetime.timedelta(days=1095)
        last_end = default_end + datetime.timedelta(days=1095)
        
        values = {
            'session': session,
            'locations': locations,
            'start_time': default_start,
            'end_time': default_end,
            'last_start': last_start,
            'last_end': last_end
        }
        
        path = os.path.join(os.path.dirname(__file__), 'locations.html')
        response = template.render(path, values)
        return response

