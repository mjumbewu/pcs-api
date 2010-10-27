from pcs.wsgi_handlers.appengine import _AppEngineBasedHandler

from pcs.wsgi_handlers.reservations import ReservationsHandler
from pcs.wsgi_handlers.reservations import ReservationHandler
from pcs.wsgi_handlers.reservations import ReservationsJsonHandler as _BaseReservationsJsonHandler

class ReservationsJsonHandler (_BaseReservationsJsonHandler, _AppEngineBasedHandler):
    pass
