import unittest
import datetime
import new

from pcs.input.wsgi import WsgiParameterError
from pcs.input.wsgi.reservations import ReservationsHandler
from pcs.input.wsgi.reservations import ReservationsHtmlHandler
from pcs.source import _ReservationsSourceInterface
from pcs.source import _SessionSourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from pcs.source.screenscrape.reservations import ReservationsScreenscrapeSource
from pcs.source.screenscrape.pcsconnection import PcsConnection
from pcs.view import _ReservationsViewInterface
from pcs.view import _ErrorViewInterface
from pcs.view.html.availability import AvailabilityHtmlView
from util.testing import patch
from util.testing import Stub
from util.TimeZone import Eastern

class ReservationsHandlerTest (unittest.TestCase):
    def setUp(self):
        # A fake request class
        class StubRequest (dict):
            pass
        
        # A fake response class
        import StringIO
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
        
        @Stub(_SessionSourceInterface)
        class StubSessionSource (object):
            pass
        
        @Stub(_ReservationsSourceInterface)
        class StubReservationsSource (object):
            pass
        
        @Stub(_ReservationsViewInterface)
        class StubReservationsView (object):
            pass
        
        @Stub(_ErrorViewInterface)
        class StubErrorView (object):
            pass
        
        self.session_source = StubSessionSource()
        self.reservation_source = StubReservationsSource()
        self.reservation_view = StubReservationsView()
        self.error_view = StubErrorView()
        
        self.request = StubRequest()
        self.response = StubResponse()
        
        self.handler = ReservationsHandler(
            self.session_source,
            self.reservation_source,
            self.reservation_view, 
            self.error_view)
        self.handler.initialize(self.request, self.response)
    
    def testShouldRespondWithReservationsAccordingToTheReservationsView(self):
        @patch(self.handler)
        def get_user_id(self):
            self.userid_called = True
            return 'user1234'
        
        @patch(self.handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
         
        @patch(self.reservation_source)
        def get_reservations(self, sessionid):
            self.sessionid = sessionid
            return 'my reservations'
        
        @patch(self.reservation_view)
        def get_reservations(self, session, reservations):
            self.session = session
            self.reservations = reservations
            return 'my reservation response'
        
        self.handler.handle_get_reservations()
        
        response = self.handler.response.out.getvalue()
        self.assert_(self.handler.userid_called)
        self.assert_(self.handler.sessionid_called)
        self.assertEqual(self.session_source.userid, 'user1234')
        self.assertEqual(self.session_source.sessionid, 'ses1234')
        self.assertEqual(self.reservation_source.sessionid, 'ses1234')
        self.assertEqual(self.reservation_view.session, 'my session')
        self.assertEqual(self.reservation_view.reservations, 'my reservations')
        self.assertEqual(response, 'my reservation response')
    
    def testShouldCallGetReservationsHandler(self):
        @patch(self.handler)
        def handle_get_reservations(self):
            self.get_handler_called = True
        
        self.handler.get()
        
        self.assert_(self.handler.get_handler_called)

def ReservationsScreenscrapeSourceTest (unittest.TestCase):
    def setUp(self):
        self.source = ReservationsScreenscrapeSource()
    
    def testShouldGetReservationDocumentFromPcsConnection(self):
        self.source.get_reservations(sessionid)

