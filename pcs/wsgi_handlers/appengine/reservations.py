from pcs.wsgi_handlers.appengine import _AppEngineBasedHandler

from pcs.wsgi_handlers.reservations import ReservationsHandler
from pcs.wsgi_handlers.reservations import ReservationHandler
from pcs.wsgi_handlers.reservations import ReservationsJsonHandler as _BaseReservationsJsonHandler
from pcs.wsgi_handlers.reservations import ReservationJsonHandler as _BaseReservationJsonHandler

class ReservationsJsonHandler (_BaseReservationsJsonHandler, _AppEngineBasedHandler):
    pass

class ReservationJsonHandler (_BaseReservationJsonHandler, _AppEngineBasedHandler):
    pass

