import unittest

from util.testing import Stub
from util.testing import patch

from pcs.wsgi_handlers.appengine.session import SessionJsonHandler
class AppEngineSessionJsonHandlerTest (unittest.TestCase):
    def test_BaseSessionHandlerShouldComeFirstInBases(self):
        from pcs.wsgi_handlers.session import SessionJsonHandler as base
        self.assertEqual(SessionJsonHandler.__bases__[0], base)

from pcs.wsgi_handlers.appengine.locations import LocationsJsonHandler
class AppEngineLocationsJsonHandlerTest (unittest.TestCase):
    def test_BaseLocationsHandlerShouldComeFirstInBases(self):
        from pcs.wsgi_handlers.locations import LocationsJsonHandler as base
        self.assertEqual(LocationsJsonHandler.__bases__[0], base)

from pcs.wsgi_handlers.appengine.reservations import ReservationsJsonHandler
class AppEngineReservationsJsonHandlerTest (unittest.TestCase):
    def test_BaseReservationsHandlerShouldComeFirstInBases(self):
        from pcs.wsgi_handlers.reservations import ReservationsJsonHandler as base
        self.assertEqual(ReservationsJsonHandler.__bases__[0], base)

from pcs.wsgi_handlers.appengine.availability import LocationAvailabilityJsonHandler
class AppEngineLocationAvailabilityJsonHandlerTest (unittest.TestCase):
    def test_BaseLocationAvailabilityHandlerShouldComeFirstInBases(self):
        from pcs.wsgi_handlers.availability import LocationAvailabilityJsonHandler as base
        self.assertEqual(LocationAvailabilityJsonHandler.__bases__[0], base)

class AppEngineApplicationTest (unittest.TestCase):
    def test_ApplicationModuleShouldCompile(self):
        # This is a test just to make sure that the imports and class names in
        # the application module are correct.
        import pcs.appengine_app
