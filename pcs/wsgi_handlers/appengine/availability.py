from pcs.wsgi_handlers.appengine import _AppEngineBasedHandler

from pcs.wsgi_handlers.availability import LocationAvailabilityJsonHandler as _BaseLocationAvailabilityJsonHandler
from pcs.wsgi_handlers.availability import VehicleAvailabilityJsonHandler as _BaseVehicleAvailabilityJsonHandler
from pcs.wsgi_handlers.availability import LocationAvailabilityHandler
from pcs.wsgi_handlers.availability import VehicleAvailabilityHandler

class LocationAvailabilityJsonHandler (_BaseLocationAvailabilityJsonHandler, _AppEngineBasedHandler):
    pass

class VehicleAvailabilityJsonHandler (_BaseVehicleAvailabilityJsonHandler, _AppEngineBasedHandler):
    pass
