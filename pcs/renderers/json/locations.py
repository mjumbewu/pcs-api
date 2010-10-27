import datetime
import os

from google.appengine.ext.webapp import template

from pcs.renderers import _LocationsViewInterface
from util.abstract import override
from util.TimeZone import Eastern

class LocationsJsonView (_LocationsViewInterface):
    @override
    def render_locations(self, session, locations):
        
        values = {
            'session': session,
            'locations': locations,
        }
        
        path = os.path.join(os.path.dirname(__file__), 'locations.json')
        response = template.render(path, values)
        return response

