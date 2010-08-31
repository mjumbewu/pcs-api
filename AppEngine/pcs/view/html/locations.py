import datetime
import os

from google.appengine.ext.webapp import template

from pcs.view import _LocationsViewInterface
from util.abstract import override

class LocationsHtmlView (_LocationsViewInterface):
    def get_locations(self, session, locations):
        values = {
            'session': session,
            'locations': locations
        }
        
        path = os.path.join(os.path.dirname(__file__), 'locations.html')
        response = template.render(path, values)
        return response

