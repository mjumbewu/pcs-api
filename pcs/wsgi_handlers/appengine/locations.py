from pcs.wsgi_handlers.appengine import _AppEngineBasedHandler

from pcs.wsgi_handlers.locations import LocationsHandler
from pcs.wsgi_handlers.locations import LocationsHtmlHandler
from pcs.wsgi_handlers.locations import LocationsJsonHandler as _BaseLocationsJsonHandler

class LocationsJsonHandler (_BaseLocationsJsonHandler, _AppEngineBasedHandler):
    pass
