import unittest
import datetime
import new

from pcs.wsgi_handlers.base import WsgiParameterError
from pcs.wsgi_handlers.appengine.reservations import ReservationsHandler
from pcs.wsgi_handlers.appengine.reservations import ReservationsJsonHandler
from pcs.fetchers import _ReservationsSourceInterface
from pcs.fetchers import _SessionSourceInterface
from pcs.fetchers.screenscrape import ScreenscrapeParseError
from pcs.fetchers.screenscrape.reservations import ReservationsScreenscrapeSource
from pcs.fetchers.screenscrape.pcsconnection import PcsConnection
from pcs.renderers import _ReservationsViewInterface
from pcs.renderers import _ErrorViewInterface
from pcs.renderers.json.reservations import ReservationsJsonView
from util.BeautifulSoup import BeautifulSoup
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
        
        class StubSessionSource (object):
            pass
        StubSessionSource = Stub(_SessionSourceInterface)(StubSessionSource)
        
        class StubReservationsSource (object):
            pass
        StubReservationsSource = Stub(_ReservationsSourceInterface)(StubReservationsSource)
        
        class StubReservationsView (object):
            pass
        StubReservationsView = Stub(_ReservationsViewInterface)(StubReservationsView)
        
        class StubErrorView (object):
            pass
        StubErrorView = Stub(_ErrorViewInterface)(StubErrorView)
        
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
        self.handler.request = self.request
        self.handler.response = self.response
    
    def testShouldPassDateStructureToReservationSource(self):
        self.request.cookies = {
            'session':r'"{\"user\":\"123\",\"id\":\"456\"}"'
        }
        
        self.request['period'] = '2010-09'
        
        @patch(self.session_source)
        def fetch_session(self, userid, sessionid):
            pass
        
        @patch(self.reservation_view)
        def render_reservations(self, session, reservations, page_num, total_pages):
            pass
        
        @patch(self.reservation_source)
        def fetch_reservations(self, sessionid, year_month=None):
            self.year_month = year_month
            return (None,None,None)
        
        self.handler.get()
        self.assertEqual(type(self.reservation_source.year_month).__name__, datetime.datetime.__name__)
        
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
        def fetch_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
         
        @patch(self.reservation_source)
        def fetch_reservations(self, sessionid, year_month=None):
            self.sessionid = sessionid
            self.year_month = year_month
            return 'my reservations', 2, 5
        
        @patch(self.reservation_view)
        def render_reservations(self, session, reservations, page_num, total_pages):
            self.session = session
            self.reservations = reservations
            return 'my reservation response'
        
        self.handler.get()
        
        response = self.handler.response.out.getvalue()
        self.assert_(self.handler.userid_called)
        self.assert_(self.handler.sessionid_called)
        self.assertEqual(self.session_source.userid, 'user1234')
        self.assertEqual(self.session_source.sessionid, 'ses1234')
        self.assertEqual(self.reservation_source.sessionid, 'ses1234')
        self.assertEqual(self.reservation_source.year_month, None)
        self.assertEqual(self.reservation_view.session, 'my session')
        self.assertEqual(self.reservation_view.reservations, 'my reservations')
        self.assertEqual(response, 'my reservation response')

class ReservationsScreenscrapeSourceTest (unittest.TestCase):
    def setUp(self):
        self.source = ReservationsScreenscrapeSource()
    
    def testShouldInferCorrectPageNumberAndPageCount(self):
        from strings_for_testing import \
            PAST_RESERVATIONS_FIRST_OF_TWO_PAGES, \
            PAST_RESERVATIONS_SECOND_OF_TWO_PAGES, \
            PAST_RESERVATIONS_SECOND_OF_FIVE_PAGES, \
            PAST_RESERVATIONS_SINGLE_PAGE
        
        first_page = BeautifulSoup(PAST_RESERVATIONS_FIRST_OF_TWO_PAGES)
        cur_page, num_pages = self.source.get_page_data_from_html_data(first_page)
        self.assertEqual(cur_page, 1)
        self.assertEqual(num_pages, 2)
        
        second_page = BeautifulSoup(PAST_RESERVATIONS_SECOND_OF_TWO_PAGES)
        cur_page, num_pages = self.source.get_page_data_from_html_data(second_page)
        self.assertEqual(cur_page, 2)
        self.assertEqual(num_pages, 2)
        
        second_page = BeautifulSoup(PAST_RESERVATIONS_SECOND_OF_FIVE_PAGES)
        cur_page, num_pages = self.source.get_page_data_from_html_data(second_page)
        self.assertEqual(cur_page, 2)
        self.assertEqual(num_pages, 5)
        
        single_page = BeautifulSoup(PAST_RESERVATIONS_SINGLE_PAGE)
        cur_page, num_pages = self.source.get_page_data_from_html_data(single_page)
        self.assertEqual(cur_page, 1)
        self.assertEqual(num_pages, 1)
    
    def testShouldCreateAPcsConnection(self):
        conn = self.source.get_pcs_connection()
        self.assertEqual(conn.__class__.__name__, 'PcsConnection')
    
    def testShouldReturnUpcomingBodyAndHeadFromPcsConnection(self):
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.url = url
                self.method = method
                self.data = data
                self.headers = headers
                class StubResponse (object):
                    def getheaders(self): return 'my headers'
                    def read(self): return 'my body'
                return StubResponse()
        StubConnection = Stub(PcsConnection)(StubConnection)
        
        conn = StubConnection()
        sessionid = 'ses1234'
        
        body, head = self.source.upcoming_reservations_from_pcs(conn, sessionid)
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/my_reservations.php?mv_action=main')
        self.assertEqual(conn.method, 'GET')
        self.assertEqual(conn.data, {})
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    def testShouldReturnPastBodyAndHeadFromPcsConnection(self):
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.url = url
                self.method = method
                self.data = data
                self.headers = headers
                class StubResponse (object):
                    def getheaders(self): return 'my headers'
                    def read(self): return 'my body'
                return StubResponse()
        StubConnection = Stub(PcsConnection)(StubConnection)
        
        conn = StubConnection()
        sessionid = 'ses1234'
        
        body, head = self.source.past_reservations_from_pcs(conn, sessionid, 2010, 10)
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/my_reservations.php?mv_action=main&main[multi_filter][history][yearmonth]=201010')
        self.assertEqual(conn.method, 'GET')
        self.assertEqual(conn.data, {})
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    def testShouldReturnEmptyReservationsListWhenNoUpcomingReservationsBodyReturnedFromPcs(self):
        from strings_for_testing import NO_UPCOMING_RESERVATIONS_BODY
        
        html_data = BeautifulSoup(NO_UPCOMING_RESERVATIONS_BODY)
        reservations = self.source.get_reservation_data_from_html_data(html_data)
        
        self.assertEqual(len(reservations), 0)
    
    def testShouldReturnOneUpcomingReservationInAppropriateSituation(self):
        from strings_for_testing import ONE_UPCOMING_RESERVATION
        
        html_data = BeautifulSoup(ONE_UPCOMING_RESERVATION)
        reservations = self.source.get_reservation_data_from_html_data(html_data)
        
        self.assertEqual(len(reservations), 1)
        reservation = reservations[0]
        self.assertEqual(reservation.id, '2472498')
        self.assertEqual(reservation.start_time, datetime.datetime(2010,9,15,6,0,tzinfo=Eastern))
        self.assertEqual(reservation.price.total_amount, 3.24)
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Baltimore')
    
    def testShouldtTwoReservationsInAppropriateSituation(self):
        from strings_for_testing import ONE_CURRENT_ONE_UPCOMING_RESERVATIONS
        
        html_data = BeautifulSoup(ONE_CURRENT_ONE_UPCOMING_RESERVATIONS)
        reservations = self.source.get_reservation_data_from_html_data(html_data)
        
        self.assertEqual(len(reservations), 2)
        
        reservation = reservations[0]
        self.assertEqual(reservation.id, '2472500')
        self.assertEqual(reservation.start_time, datetime.datetime(2010,9,15,0,45,tzinfo=Eastern))
        self.assertEqual(reservation.price.total_amount, 3.24)
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Baltimore')
        
        reservation = reservations[1]
        self.assertEqual(reservation.id, '2472498')
        self.assertEqual(reservation.start_time, datetime.datetime(2010,9,15,6,0,tzinfo=Eastern))
        self.assertEqual(reservation.price.total_amount, 3.24)
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Baltimore')
    
    def testShouldReturnUpcomingReservationsResponseBodyAccordingToConnectionResponseIfNoExceptionsRaised(self):
        self.source.past_res_called = False
        self.source.upcoming_res_called = False
        
        @patch(self.source)
        def get_pcs_connection(self):
            self.pcs_conn_called = True
            return 'my connection'
        
        @patch(self.source)
        def upcoming_reservations_from_pcs(self, conn, sessionid):
            self.upcoming_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            return 'my body', 'my head'
        
        @patch(self.source)
        def past_reservations_from_pcs(self, conn, sessionid, year, month):
            self.past_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            return 'my body', 'my head'
        
        @patch(self.source)
        def get_html_data(self, response_body):
            self.html_body = response_body
            return 'my html doc'
        
        @patch(self.source)
        def get_reservation_data_from_html_data(self, html_data):
            self.html_doc = html_data
            return 'my reservations'
        
        @patch(self.source)
        def get_page_data_from_html_data(self, html_data):
            return 3, 5
        
        sessionid = 'ses1234'
        driverid = 'drv1234'
        
        reservations, page, count = self.source.fetch_reservations(sessionid)
        
        self.assert_(self.source.pcs_conn_called)
        self.assert_(self.source.upcoming_res_called)
        self.assert_(not self.source.past_res_called)
        self.assertEqual(self.source.conn, 'my connection')
        self.assertEqual(self.source.sessionid, 'ses1234')
        self.assertEqual(self.source.html_body, 'my body')
        self.assertEqual(self.source.html_doc, 'my html doc')
        self.assertEqual(reservations, 'my reservations')
        self.assertEqual(page, 3)
        self.assertEqual(count, 5)
    
    def testShouldReturnPastReservationsResponseBodyAccordingToConnectionResponseIfNoExceptionsRaised(self):
        self.source.past_res_called = False
        self.source.upcoming_res_called = False
        
        @patch(self.source)
        def get_pcs_connection(self):
            self.pcs_conn_called = True
            return 'my connection'
        
        @patch(self.source)
        def upcoming_reservations_from_pcs(self, conn, sessionid):
            self.upcoming_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            return 'my body', 'my head'
        
        @patch(self.source)
        def past_reservations_from_pcs(self, conn, sessionid, year, month):
            self.past_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            self.year = year
            self.month = month
            return 'my body', 'my head'
        
        @patch(self.source)
        def get_html_data(self, response_body):
            self.html_body = response_body
            return 'my html doc'
        
        @patch(self.source)
        def get_reservation_data_from_html_data(self, html_data):
            self.html_doc = html_data
            return 'my reservations'
        
        @patch(self.source)
        def get_page_data_from_html_data(self, html_data):
            return 3, 5
        
        sessionid = 'ses1234'
        driverid = 'drv1234'
        
        reservations, page, count = self.source.fetch_reservations(sessionid, datetime.date(2010, 11, 1))
        
        self.assert_(self.source.pcs_conn_called)
        self.assert_(not self.source.upcoming_res_called)
        self.assert_(self.source.past_res_called)
        self.assertEqual(self.source.conn, 'my connection')
        self.assertEqual(self.source.year, 2010)
        self.assertEqual(self.source.month, 11)
        self.assertEqual(self.source.sessionid, 'ses1234')
        self.assertEqual(self.source.html_body, 'my body')
        self.assertEqual(self.source.html_doc, 'my html doc')
        self.assertEqual(reservations, 'my reservations')
        self.assertEqual(page, 3)
        self.assertEqual(count, 5)
    
    def testShouldCreateReservationPastBasedOnContentsOfTableRow(self):
        tr_str = r"""<tr class="zebra"><td >2460589</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=6&pk=5736346"    >47th & Pine - Prius Liftback</a></td> 
<td >12:45 pm Wednesday, September 1, 2010</td><td >4:45 pm Wednesday, September 1, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$29.28</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$17.80&nbsp;(Time)&nbsp;+<br/>$7.00&nbsp;(Distance&nbsp;@&nbsp;28&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$4.48&nbsp;(Tax)</span></td><td >Normal</td><td >rasheed</td></tr>"""
        tr = BeautifulSoup(tr_str)
        
        reservation = self.source.get_reservation_from_table_row_data(tr)
        from pcs.data.reservation import ReservationStatus
        self.assertEqual(reservation.id, '2460589')
        self.assertEqual(reservation.vehicle.pod.id, '5736346')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Pine')
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.start_time.timetuple()[:6], (2010,9,1,12,45,0))
        self.assertEqual(reservation.end_time.timetuple()[:6], (2010,9,1,16,45,0))
        self.assertEqual(reservation.status, ReservationStatus.PAST)

class ReservationsJsonHandlerTest (unittest.TestCase):
    def testShouldUseScreenscrapeFetchersAndJsonRenderers(self):
        handler = ReservationsJsonHandler()
        
        self.assertEqual(handler.error_view.__class__.__name__, 
            'ErrorJsonView')
        self.assertEqual(handler.reservation_source.__class__.__name__,
            'ReservationsScreenscrapeSource')
        self.assertEqual(handler.reservation_view.__class__.__name__,
            'ReservationsJsonView')

class ReservationsJsonViewTest (unittest.TestCase):
    def testShouldRenderReservationListJson(self):
        renderer = ReservationsJsonView()
        
        class StubObject (object):
            pass
        
        session = StubObject()
        session.id = 'ses123'
        session.user = 'user123'
        session.name = 'user name'
        
        res1 = StubObject()
        res1.id = 'res1'
        res1.start_time = datetime.datetime(2010, 11, 15, 16, 30, tzinfo=Eastern)
        res1.end_time = datetime.datetime(2010, 11, 15, 17, 15, tzinfo=Eastern)
        res1.vehicle = StubObject()
        res1.vehicle.id = 'v123'
        res1.vehicle.model = StubObject()
        res1.vehicle.model.name = 'model 1'
        res1.vehicle.pod = StubObject()
        res1.vehicle.pod.id = 'pod123'
        res1.vehicle.pod.name = 'pod 1'
        
        res2 = StubObject()
        res2.id = 'res2'
        res2.start_time = datetime.datetime(2010, 12, 30, 16, 30, tzinfo=Eastern)
        res2.end_time = datetime.datetime(2010, 12, 31, 17, 15, tzinfo=Eastern)
        res2.vehicle = StubObject()
        res2.vehicle.id = 'v123'
        res2.vehicle.model = StubObject()
        res2.vehicle.model.name = 'model 1'
        res2.vehicle.pod = StubObject()
        res2.vehicle.pod.id = 'pod123'
        res2.vehicle.pod.name = 'pod 1'
        
        reservations = [res1, res2]
        
        result = renderer.render_reservations(None, reservations, 1, 2)
        
        expected = \
"""{
  "reservation_list": {
    "num_pages": 2, 
    "page": 1, 
    "reservations": [
      {
        "end_time": "2010-11-15T17:15", 
        "id": "res1", 
        "start_time": "2010-11-15T16:30", 
        "vehicle": {
          "id": "v123", 
          "model": {
            "name": "model 1"
          }, 
          "pod": {
            "id": "pod123", 
            "name": "pod 1"
          }
        }
      }, 
      {
        "end_time": "2010-12-31T17:15", 
        "id": "res2", 
        "start_time": "2010-12-30T16:30", 
        "vehicle": {
          "id": "v123", 
          "model": {
            "name": "model 1"
          }, 
          "pod": {
            "id": "pod123", 
            "name": "pod 1"
          }
        }
      }
    ]
  }
}"""
        self.assertEqual(result, expected)

