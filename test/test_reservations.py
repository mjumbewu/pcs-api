import unittest
import datetime
import new

from pcs.wsgi_handlers.base import WsgiParameterError
from pcs.wsgi_handlers.appengine.reservations import ReservationHandler
from pcs.wsgi_handlers.appengine.reservations import ReservationsHandler
from pcs.wsgi_handlers.appengine.reservations import ReservationJsonHandler
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

# A fake request class
class StubRequest (dict):
    def __init__(self):
        self.headers = {}
        self.query_string = ''
        self.body = ''
        self.cookies = {}
    def arguments(self):
        return []

# A fake response class
import StringIO
class StubResponse (object):
    def __init__(self):
        self.out = StringIO.StringIO()
    def set_status(self, status):
        self.status = status

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

class ReservationsHandlerTest (unittest.TestCase):
    def setUp(self):
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
            'session_id':r'456'
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
        self.assert_(self.handler.sessionid_called)
        self.assertEqual(self.reservation_source.sessionid, 'ses1234')
        self.assertEqual(self.reservation_source.year_month, None)
        self.assertEqual(self.reservation_view.reservations, 'my reservations')
        self.assertEqual(response, 'my reservation response')
    
    def testShouldConfirmValidReservation(self):
        @patch(self.handler)
        def get_user_id(self):
            return 'user1234'
        
        @patch(self.handler)
        def get_session_id(self):
            return 'ses1234'
        
        @patch(self.handler)
        def get_vehicle_id(self):
            return 'vid1234'
        
        @patch(self.session_source)
        def fetch_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
        
        @patch(self.reservation_source)
        def fetch_reservation_creation(self, sessionid, vehicleid, start_time, end_time, reservation_memo):
            self.sessionid = sessionid
            self.vehicleid = vehicleid
            self.start = start_time
            self.end = end_time
            self.memo = reservation_memo
            return 'my reservation'
        
        @patch(self.reservation_view)
        def render_confirmation(self, session, reservation, event):
            self.session = session
            self.reservation = reservation
            self.event = event
            return 'my confirmation'
        
        self.error_view.render_called = False
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            self.render_called = True
            return str('\n' + error_detail + '\n' + error_msg)
        
        self.handler.post()
        
        response = self.handler.response.out.getvalue()
        self.assert_(not self.error_view.render_called, response)
        self.assertEqual(response, 'my confirmation')

class ReservationHandlerTest (unittest.TestCase):
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
        
        self.handler = ReservationHandler(
            self.session_source,
            self.reservation_source,
            self.reservation_view, 
            self.error_view)
        self.handler.request = self.request
        self.handler.response = self.response
    
    def testPutHandlerShouldOrchestrateDataPassingCorrectly(self):
        @patch(self.handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(self.handler)
        def get_time_range(self):
            self.timerange_called = True
            return 100, 1000
        
        @patch(self.handler)
        def get_vehicle_id(self):
            self.vehicleid_called = True
            return 'vid1234'
        
        @patch(self.handler)
        def get_reservation_memo(self):
            self.memo_called = True
            return 'reservation memo'
        
        @patch(self.reservation_source)
        def fetch_reservation_modification(self, sessionid, liveid, vehicleid, start_time, end_time, reservation_memo):
            self.sessionid = sessionid
            self.liveid = liveid
            self.vehicleid = vehicleid
            self.start = start_time
            self.end = end_time
            self.memo = reservation_memo
            return 'my reservation'
        
        @patch(self.reservation_view)
        def render_confirmation(self, session, reservation, event):
            self.event = event
            self.reservation = reservation
            return 'my confirmation response'
        
        self.error_view.render_called = False
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            self.render_called = True
            return str('\n' + error_detail + '\n' + error_msg)
        
        self.handler.put('live1234')
        
        response = self.handler.response.out.getvalue()
        self.assert_(not self.error_view.render_called, response)
        self.assert_(self.handler.sessionid_called)
        self.assert_(self.handler.vehicleid_called)
        self.assert_(self.handler.timerange_called)
        self.assert_(self.handler.memo_called)
        self.assertEqual(self.reservation_source.sessionid, 'ses1234')
        self.assertEqual(self.reservation_source.liveid, 'live1234')
        self.assertEqual(self.reservation_source.vehicleid, 'vid1234')
        self.assertEqual(self.reservation_source.start, 100)
        self.assertEqual(self.reservation_source.end, 1000)
        self.assertEqual(self.reservation_source.memo, 'reservation memo')
        self.assertEqual(self.reservation_view.event, 'modify')
        self.assertEqual(self.reservation_view.reservation, 'my reservation')
        self.assertEqual(response, 'my confirmation response')
    
    def testDeleteHandlerShouldOrchestrateDataPassingCorrectly(self):
        @patch(self.handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(self.handler)
        def get_time_range(self):
            self.timerange_called = True
            return 100, 1000
        
        @patch(self.handler)
        def get_vehicle_id(self):
            self.vehicleid_called = True
            return 'vid1234'
        
        @patch(self.reservation_source)
        def fetch_reservation_cancellation(self, sessionid, liveid, vehicleid, start_time, end_time):
            self.sessionid = sessionid
            self.liveid = liveid
            self.vehicleid = vehicleid
            self.start = start_time
            self.end = end_time
            return 'my reservation'
        
        @patch(self.reservation_view)
        def render_confirmation(self, session, reservation, event):
            self.event = event
            self.reservation = reservation
            return 'my confirmation response'
        
        self.error_view.render_called = False
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            self.render_called = True
            return str('\n' + error_detail + '\n' + error_msg)
        
        self.handler.delete('live1234')
        
        response = self.handler.response.out.getvalue()
        self.assert_(not self.error_view.render_called, response)
        self.assert_(self.handler.sessionid_called)
        self.assert_(self.handler.vehicleid_called)
        self.assert_(self.handler.timerange_called)
        self.assertEqual(self.reservation_source.sessionid, 'ses1234')
        self.assertEqual(self.reservation_source.liveid, 'live1234')
        self.assertEqual(self.reservation_source.vehicleid, 'vid1234')
        self.assertEqual(self.reservation_source.start, 100)
        self.assertEqual(self.reservation_source.end, 1000)
        self.assertEqual(self.reservation_view.event, 'cancel')
        self.assertEqual(self.reservation_view.reservation, 'my reservation')
        self.assertEqual(response, 'my confirmation response')
    
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
        cur_page, num_pages = self.source.decoder.decode_page_info_from_log_doc(first_page)
        self.assertEqual(cur_page, 1)
        self.assertEqual(num_pages, 2)
        
        second_page = BeautifulSoup(PAST_RESERVATIONS_SECOND_OF_TWO_PAGES)
        cur_page, num_pages = self.source.decoder.decode_page_info_from_log_doc(second_page)
        self.assertEqual(cur_page, 2)
        self.assertEqual(num_pages, 2)
        
        second_page = BeautifulSoup(PAST_RESERVATIONS_SECOND_OF_FIVE_PAGES)
        cur_page, num_pages = self.source.decoder.decode_page_info_from_log_doc(second_page)
        self.assertEqual(cur_page, 2)
        self.assertEqual(num_pages, 5)
        
        single_page = BeautifulSoup(PAST_RESERVATIONS_SINGLE_PAGE)
        cur_page, num_pages = self.source.decoder.decode_page_info_from_log_doc(single_page)
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
        
        body, head = self.source.requester.request_upcoming_reservations_from_pcs(conn, sessionid)
        
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/my_reservations.php?mv_action=main')
        self.assertEqual(conn.method, 'GET')
        self.assertEqual(conn.data, {})
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
    
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
        
        body, head = self.source.requester.request_past_reservations_from_pcs(conn, sessionid, 2010, 10)
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/my_reservations.php?mv_action=main&main[multi_filter][history][yearmonth]=201010')
        self.assertEqual(conn.method, 'GET')
        self.assertEqual(conn.data, {})
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    def testShouldReturnEmptyReservationsListWhenNoUpcomingReservationsBodyReturnedFromPcs(self):
        from strings_for_testing import NO_UPCOMING_RESERVATIONS_BODY
        
        html_document = BeautifulSoup(NO_UPCOMING_RESERVATIONS_BODY)
        reservations = self.source.decoder.build_reservation_log_from_log_doc(html_document)
        
        self.assertEqual(len(reservations), 0)
    
    def testShouldReturnOneUpcomingReservationInAppropriateSituation(self):
        from strings_for_testing import ONE_UPCOMING_RESERVATION
        
        html_document = BeautifulSoup(ONE_UPCOMING_RESERVATION)
        reservations = self.source.decoder.build_reservation_log_from_log_doc(html_document)
        
        self.assertEqual(len(reservations), 1)
        reservation = reservations[0]
        self.assertEqual(reservation.logid, '2472498')
        self.assertEqual(reservation.start_time, datetime.datetime(2010,9,15,6,0,tzinfo=Eastern))
        self.assertEqual(reservation.price.total_amount, 3.24)
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Baltimore')
    
    def testShouldtTwoReservationsInAppropriateSituation(self):
        from strings_for_testing import ONE_CURRENT_ONE_UPCOMING_RESERVATIONS
        
        html_document = BeautifulSoup(ONE_CURRENT_ONE_UPCOMING_RESERVATIONS)
        reservations = self.source.decoder.build_reservation_log_from_log_doc(html_document)
        
        self.assertEqual(len(reservations), 2)
        
        reservation = reservations[0]
        self.assertEqual(reservation.logid, '2472500')
        self.assertEqual(reservation.start_time, datetime.datetime(2010,9,15,0,45,tzinfo=Eastern))
        self.assertEqual(reservation.price.total_amount, 3.24)
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Baltimore')
        
        reservation = reservations[1]
        self.assertEqual(reservation.logid, '2472498')
        self.assertEqual(reservation.start_time, datetime.datetime(2010,9,15,6,0,tzinfo=Eastern))
        self.assertEqual(reservation.price.total_amount, 3.24)
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Baltimore')
    
    def testShouldReturnUpcomingReservationsResponseBodyAccordingToConnectionResponseIfNoExceptionsRaised(self):
        self.source.requester.past_res_called = False
        self.source.requester.upcoming_res_called = False
        
        @patch(self.source)
        def get_pcs_connection(self):
            self.pcs_conn_called = True
            return 'my connection'
        
        @patch(self.source.requester)
        def request_upcoming_reservations_from_pcs(self, conn, sessionid):
            self.upcoming_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            return 'my body', 'my head'
        
        @patch(self.source.requester)
        def request_past_reservations_from_pcs(self, conn, sessionid, year, month):
            self.past_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            return 'my body', 'my head'
        
        @patch(self.source)
        def get_html_document(self, response_body):
            self.html_body = response_body
            return 'my html doc'
        
        @patch(self.source.decoder)
        def build_reservation_log_from_log_doc(self, html_document):
            self.html_doc = html_document
            return 'my reservations'
        
        @patch(self.source.decoder)
        def decode_page_info_from_log_doc(self, html_document):
            return 3, 5
        
        sessionid = 'ses1234'
        driverid = 'drv1234'
        
        reservations, page, count = self.source.fetch_reservations(sessionid)
        
        self.assert_(self.source.pcs_conn_called)
        self.assert_(self.source.requester.upcoming_res_called)
        self.assert_(not self.source.requester.past_res_called)
        self.assertEqual(self.source.requester.conn, 'my connection')
        self.assertEqual(self.source.requester.sessionid, 'ses1234')
        self.assertEqual(self.source.html_body, 'my body')
        self.assertEqual(self.source.decoder.html_doc, 'my html doc')
        self.assertEqual(reservations, 'my reservations')
        self.assertEqual(page, 3)
        self.assertEqual(count, 5)
    
    def testShouldReturnPastReservationsResponseBodyAccordingToConnectionResponseIfNoExceptionsRaised(self):
        self.source.requester.past_res_called = False
        self.source.requester.upcoming_res_called = False
        
        @patch(self.source)
        def get_pcs_connection(self):
            self.pcs_conn_called = True
            return 'my connection'
        
        @patch(self.source.requester)
        def request_upcoming_reservations_from_pcs(self, conn, sessionid):
            self.upcoming_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            return 'my body', 'my head'
        
        @patch(self.source.requester)
        def request_past_reservations_from_pcs(self, conn, sessionid, year, month):
            self.past_res_called = True
            self.conn = conn
            self.sessionid = sessionid
            self.year = year
            self.month = month
            return 'my body', 'my head'
        
        @patch(self.source)
        def get_html_document(self, response_body):
            self.html_body = response_body
            return 'my html doc'
        
        @patch(self.source.decoder)
        def build_reservation_log_from_log_doc(self, html_document):
            self.html_doc = html_document
            return 'my reservations'
        
        @patch(self.source.decoder)
        def decode_page_info_from_log_doc(self, html_document):
            return 3, 5
        
        sessionid = 'ses1234'
        driverid = 'drv1234'
        
        reservations, page, count = self.source.fetch_reservations(sessionid, datetime.date(2010, 11, 1))
        
        self.assert_(self.source.pcs_conn_called)
        self.assert_(not self.source.requester.upcoming_res_called)
        self.assert_(self.source.requester.past_res_called)
        self.assertEqual(self.source.requester.conn, 'my connection')
        self.assertEqual(self.source.requester.year, 2010)
        self.assertEqual(self.source.requester.month, 11)
        self.assertEqual(self.source.requester.sessionid, 'ses1234')
        self.assertEqual(self.source.html_body, 'my body')
        self.assertEqual(self.source.decoder.html_doc, 'my html doc')
        self.assertEqual(reservations, 'my reservations')
        self.assertEqual(page, 3)
        self.assertEqual(count, 5)
    
    def testShouldFetchReservationPastBasedOnContentsOfTableRow(self):
        tr_str = r"""<tr class="zebra"><td >2460589</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=6&pk=5736346"    >47th & Pine - Prius Liftback</a></td> 
<td >12:45 pm Wednesday, September 1, 2010</td><td >4:45 pm Wednesday, September 1, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$29.28</a> 
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$17.80&nbsp;(Time)&nbsp;+<br/>$7.00&nbsp;(Distance&nbsp;@&nbsp;28&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$4.48&nbsp;(Tax)</span></td><td >Normal</td><td >rasheed</td></tr>"""
        tr = BeautifulSoup(tr_str)
        
        reservation = self.source.decoder.build_reservation_from_table_row_element(tr)
        from pcs.data.reservation import ReservationStatus
        self.assertEqual(reservation.logid, '2460589')
        self.assertEqual(reservation.vehicle.pod.id, '5736346')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Pine')
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.start_time.timetuple()[:6], (2010,9,1,12,45,0))
        self.assertEqual(reservation.end_time.timetuple()[:6], (2010,9,1,16,45,0))
        self.assertEqual(reservation.status, ReservationStatus.PAST)
    
    def testShouldFetchReservationsWithOneUpcomingInGivenMonth(self):
        from strings_for_testing import ONE_UPCOMING_RESERVATION_IN_OCTOBER
        html_document = BeautifulSoup(ONE_UPCOMING_RESERVATION_IN_OCTOBER)
        
        res_data = self.source.decoder.build_reservation_log_from_log_doc(html_document)
        
        from pcs.data.reservation import ReservationStatus
        self.assertEqual(res_data[0].logid, '2491921')
        self.assertEqual(res_data[-1].logid, '2514083')
        self.assertEqual(res_data[-1].liveid, '149337407')
    
    def testShouldCreateReservationConfirmation(self):
        from strings_for_testing import NEW_RESERVATION_CONFIRMATION
        from strings_for_testing import NEW_RESERVATION_REDIRECT_SCRIPT
        from strings_for_testing import RESERVATION_LIGHTBOX_WITH_NO_VEHICLE_INFO
        
        class StubResponse (object):
            def read(self):
                return NEW_RESERVATION_CONFIRMATION
            def getheaders(self):
                return {}
            
        class StubConnection (object):
            def request(self, *params):
                return StubResponse()
        
        @patch(self.source)
        def get_pcs_connection(self):
            return StubConnection()
        
        @patch(self.source.requester)
        def request_create_reservation_from_pcs(self, conn, sessionid, vehicleid, transactionid, start_time, end_time, reservation_memo):
            return NEW_RESERVATION_REDIRECT_SCRIPT, None
        
        @patch(self.source.requester)
        def request_empty_create_reservation_box_from_pcs(self, conn, sessionid, transtype, liveid=None):
            return RESERVATION_LIGHTBOX_WITH_NO_VEHICLE_INFO, None
        
        confirmation = self.source.fetch_reservation_creation(None,None,None,None,None)
    
    def testShouldPassCorrectParametersToPcsForEmptyCreateResBox(self):
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
        body, head = \
            self.source.requester.request_empty_create_reservation_box_from_pcs(conn, sessionid, 'add')
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/lightbox.php')
        self.assertEqual(conn.method, 'POST')
        self.assertEqual(conn.data, 'mv_action=add')
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    def testShouldExtractCorrectTransactionIdFromLightboxBlock(self):
        from strings_for_testing import RESERVATION_LIGHTBOX_WITH_NO_VEHICLE_INFO
        
        lgtbox_block = BeautifulSoup(RESERVATION_LIGHTBOX_WITH_NO_VEHICLE_INFO)
        transactionid = \
            self.source.decoder.decode_transaction_id_from_lightbox_block('add', lgtbox_block)
        
        self.assertEqual(transactionid, '5')
    
    def testShouldExtractCorrectReservationLiveIdFromRedirectScript(self):
        from strings_for_testing import NEW_RESERVATION_REDIRECT_SCRIPT
        
        redir_elem = BeautifulSoup(NEW_RESERVATION_REDIRECT_SCRIPT)
        liveid = \
            self.source.decoder.decode_reservation_liveid_from_redirect_script_element(redir_elem)
        
        self.assertEqual(liveid, '149385106')
    
    def testShouldExtractCorrectReservationInfoFromConfirmationDocument(self):
        from strings_for_testing import NEW_RESERVATION_CONFIRMATION
        
        conf_doc = BeautifulSoup(NEW_RESERVATION_CONFIRMATION)
        logid, modelname, podname = \
            self.source.decoder.decode_reservation_info_from_confirmation_doc(conf_doc)
        
        self.assertEqual(logid, '2516709')
        self.assertEqual(modelname, 'Prius Liftback')
        self.assertEqual(podname, '47th & Baltimore')
    
    def testShouldBuildCorrectReservationFromGivenInformation(self):
        logid = 'logid1234'
        liveid = 'liveid5678'
        start_time = 100
        end_time = 1000
        vehicleid = '0987'
        modelname = 'fancy'
        podid = 'pod0987'
        podname = 'closeby'
        
        reservation = self.source.build_reservation(logid, liveid, start_time, end_time, vehicleid, modelname, podid, podname)
        
        self.assertEqual(reservation.logid, logid)
        self.assertEqual(reservation.liveid, liveid)
        self.assertEqual(reservation.start_time, start_time)
        self.assertEqual(reservation.end_time, end_time)
        self.assertEqual(reservation.vehicle.id, vehicleid)
        self.assertEqual(reservation.vehicle.model.name, modelname)
        self.assertEqual(reservation.vehicle.pod.id, podid)
        self.assertEqual(reservation.vehicle.pod.name, podname)
    
    def testShouldBuildCorrectVehicleFromGivenInformation(self):
        vehicleid = 'vid1234'
        modelname = 'Prius'
        podid = 'pod5678'
        podname = '47th & Baltimore'
        
        vehicle = self.source.build_vehicle(vehicleid, modelname, podid, podname)
        self.assertEqual(vehicle.id, vehicleid)
        self.assertEqual(vehicle.model.name, modelname)
        self.assertEqual(vehicle.pod.id, podid)
        self.assertEqual(vehicle.pod.name, podname)
    
    def testModifyResShouldCoordinateParameterPassingCorrectly(self):
        # Verify the orchestration that the modify_reservation method is doing.
        sessionid = 'ses1234'
        liveid = 'live1234'
        vehicleid = 'vid1234'
        start_time = datetime.datetime(2010,12,6,3,30)
        end_time = datetime.datetime(2010,12,6,5,15)
        memo = 'my modified reservation'
        
        self.source.transactionid_called = False
        @patch(self.source)
        def get_a_transaction_id(self, conn, sessionid, transtype, liveid=None):
            self.transactionid_called = True
            return 'tid1234'
        
        self.source.modify_res_called = False
        @patch(self.source)
        def send_modification_info(self, conn, sessionid, liveid, transactionid, vehicleid, start_time, end_time, memo):
            self.modify_res_called = True
            self.mod_sessionid = sessionid
            self.mod_liveid = liveid
            self.mod_vid = vehicleid
            self.mod_start = start_time
            self.mod_end = end_time
            self.mod_memo = memo
            return 'live5678'
        
        self.source.res_info_called = False
        @patch(self.source)
        def get_reservation_information(self, conn, sessionid, liveid):
            self.res_info_called = True
            self.res_sessionid = sessionid
            self.res_liveid = liveid
            return 'logid', 'model name', 'pod name'
        
        self.source.res_builder_called = False
        @patch(self.source)
        def build_reservation(self, logid, liveid, start_time, end_time, vehicleid, modelname, podid, podname):
            self.res_builder_called = True
            self.bld_logid = logid
            self.bld_liveid = liveid
            self.bld_vid = vehicleid
            self.bld_modname = modelname
            self.bld_podid = podid
            self.bld_podname = podname
            return 'my reservation'
        
        reservation = self.source.fetch_reservation_modification(sessionid, liveid, vehicleid, start_time, end_time, memo)
        
        self.assert_(self.source.transactionid_called)
        self.assert_(self.source.modify_res_called)
        self.assertEqual(self.source.mod_sessionid, sessionid)
        self.assertEqual(self.source.mod_liveid, liveid)
        self.assertEqual(self.source.mod_vid, vehicleid)
        self.assertEqual(self.source.mod_start, start_time)
        self.assertEqual(self.source.mod_end, end_time)
        self.assertEqual(self.source.mod_memo, memo)
        self.assert_(self.source.res_info_called)
        self.assertEqual(self.source.res_sessionid, sessionid)
        self.assertEqual(self.source.res_liveid, 'live5678')
        self.assert_(self.source.res_builder_called)
        self.assertEqual(self.source.bld_logid, 'logid')
        self.assertEqual(self.source.bld_liveid, 'live5678')
        self.assertEqual(self.source.bld_modname, 'model name')
        self.assertEqual(self.source.bld_podname, 'pod name')
        self.assertEqual(reservation, 'my reservation')
    
    def testShouldDecodeLiveIdFromModifactionRequest(self):
        conn = None
        sid = None
        liveid = None
        tid = None
        vid = None
        stime = None
        etime = None
        memo = None
        
        @patch(self.source.requester)
        def request_modify_reservation_from_pcs(self, conn, sessionid, liveid, transactionid, vehicleid, start_time, end_time, memo):
            from strings_for_testing import NEW_RESERVATION_REDIRECT_SCRIPT
            return NEW_RESERVATION_REDIRECT_SCRIPT, None
            
        liveid = \
            self.source.send_modification_info(conn, sid, liveid, tid, vid, stime, etime, memo)
        
        self.assertEqual(liveid, '149385106')
    
    def testShouldDecodeResInfoFromConfirmationRequest(self):
        conn = None
        sid = None
        liveid = None
        
        @patch(self.source.requester)
        def request_confirm_reservation_from_pcs(self, conn, sessionid, liveid):
            from strings_for_testing import NEW_RESERVATION_CONFIRMATION
            return NEW_RESERVATION_CONFIRMATION, None
            
        logid, modelname, podname = \
            self.source.get_reservation_information(conn, sid, liveid)
        
        self.assertEqual(logid, '2516709')
        self.assertEqual(modelname, 'Prius Liftback')
        self.assertEqual(podname, '47th & Baltimore')
    
    def testShouldDecodeResInfoFromCancellationRequest(self):
        conn = None
        sid = None
        liveid = None
        tid = None
        vid = None
        stime = None
        etime = None
        memo = None
        
        @patch(self.source.requester)
        def request_cancel_reservation_from_pcs(self, conn, sessionid, liveid, transactionid, vehicleid, start_time, end_time):
            from strings_for_testing import CANCELLED_RESERVATION_CONFIRMATION
            return CANCELLED_RESERVATION_CONFIRMATION, None
            
        logid, modelname, podname = \
            self.source.send_cancellation_info(conn, sid, liveid, tid, vid, stime, etime)
        
        self.assertEqual(logid, '2517617')
        self.assertEqual(modelname, 'Prius Liftback')
        self.assertEqual(podname, '47th & Baltimore')
    
    def testShouldConstructCorrectRequestForCreatingReservation(self):
        conn = StubConnection()
        
        sid = 'sid1234'
        vid = 'vid1234'
        tid = 'tid1234'
        stime = datetime.datetime(2011,3,17,16,45)
        etime = datetime.datetime(2011,3,17,17,45)
        memo = 'new reservation'
        
        body, head = \
            self.source.requester.request_create_reservation_from_pcs(conn, sid, vid, tid, stime, etime, memo)
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/lightbox.php?mv_action=add')
        self.assertEqual(conn.method, 'POST')
        self.assertEqual(conn.data, 'add%5Bend_stamp%5D%5Bend_date%5D%5Bdate%5D=03%2F17%2F11&add%5Bend_stamp%5D%5Bend_time%5D%5Btime%5D=63900&add%5Bstart_stamp%5D%5Bstart_time%5D%5Btime%5D=60300&add%5Bstart_stamp%5D%5Bstart_date%5D%5Bdate%5D=03%2F17%2F11&add%5Bstack_pk%5D=vid1234&add%5Bjob_code%5D=new+reservation&mv_action=add&add%5Btid%5D=tid1234')
        self.assertEqual(conn.headers, {'Cookie':'sid=sid1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    def testShouldConstructCorrectRequestForModifyingReservation(self):
        conn = StubConnection()
        
        sid = 'sid1234'
        liveid = 'live1234'
        vid = 'vid1234'
        tid = 'tid1234'
        stime = datetime.datetime(2011,3,17,16,45)
        etime = datetime.datetime(2011,3,17,17,45)
        memo = 'changed reservation'
        
        body, head = \
            self.source.requester.request_modify_reservation_from_pcs(conn, sid, liveid, tid, vid, stime, etime, memo)
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/lightbox.php')
        self.assertEqual(conn.method, 'POST')
        self.assertEqual(conn.data, 'edit%5Bstart_stamp%5D%5Bstart_date%5D%5Bdate%5D=03%2F17%2F11&edit%5Bstart_stamp%5D%5Bstart_time%5D%5Btime%5D=60300&edit%5Bend_stamp%5D%5Bend_date%5D%5Bdate%5D=03%2F17%2F11&edit%5Bend_stamp%5D%5Bend_time%5D%5Btime%5D=63900&edit%5Bstack_pk%5D=vid1234&edit%5Bjob_code%5D=changed+reservation&edit%5Bpk%5D=live1234&pk=live1234&edit%5Btid%5D=tid1234&mv_action=edit')
        self.assertEqual(conn.headers, {'Cookie':'sid=sid1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    def testShouldConstructCorrectRequestForCancelingReservation(self):
        conn = StubConnection()
        
        sid = 'sid1234'
        liveid = 'live1234'
        vid = 'vid1234'
        tid = 'tid1234'
        stime = datetime.datetime(2011,3,17,16,45)
        etime = datetime.datetime(2011,3,17,17,45)
        
        body, head = \
            self.source.requester.request_cancel_reservation_from_pcs(conn, sid, liveid, tid, vid, stime, etime)
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/my_reservations.php')
        self.assertEqual(conn.method, 'POST')
        self.assertEqual(conn.data, 'do_cancel%5Bstart_stamp%5D%5Bstart_time%5D%5Btime%5D=60300&do_cancel%5Bend_stamp%5D%5Bend_time%5D%5Btime%5D=63900&do_cancel%5Bend_stamp%5D%5Bend_date%5D%5Bdate%5D=03%2F17%2F11&do_cancel%5Bstart_stamp%5D%5Bstart_date%5D%5Bdate%5D=03%2F17%2F11&do_cancel%5Bstack_pk%5D=vid1234&do_cancel%5Bpk%5D=live1234&pk=live1234&do_cancel%5Btid%5D=tid1234&mv_action=do_cancel')
        self.assertEqual(conn.headers, {'Cookie':'sid=sid1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    def testModifyResShouldCoordinateParameterPassingCorrectly(self):
        # Verify the orchestration that the modify_reservation method is doing.
        sessionid = 'ses1234'
        liveid = 'live1234'
        vehicleid = 'vid1234'
        start_time = datetime.datetime(2010,12,6,3,30)
        end_time = datetime.datetime(2010,12,6,5,15)
        
        self.source.transactionid_called = False
        @patch(self.source)
        def get_a_transaction_id(self, conn, sessionid, transtype, liveid=None):
            self.transactionid_called = True
            self.trn_type = transtype
            self.trn_liveid = liveid
            return 'tid1234'
        
        self.source.cancel_res_called = False
        @patch(self.source)
        def send_cancellation_info(self, conn, sessionid, liveid, transactionid, vehicleid, start_time, end_time):
            self.cancel_res_called = True
            self.can_sessionid = sessionid
            self.can_liveid = liveid
            self.can_vid = vehicleid
            self.can_start = start_time
            self.can_end = end_time
            return 'logid', 'model name', 'pod name'
        
        self.source.res_builder_called = False
        @patch(self.source)
        def build_reservation(self, logid, liveid, start_time, end_time, vehicleid, modelname, podid, podname):
            self.res_builder_called = True
            self.bld_logid = logid
            self.bld_liveid = liveid
            self.bld_vid = vehicleid
            self.bld_modname = modelname
            self.bld_podid = podid
            self.bld_podname = podname
            return 'my reservation'
        
        reservation = self.source.fetch_reservation_cancellation(sessionid, liveid, vehicleid, start_time, end_time)
        
        self.assert_(self.source.transactionid_called)
        self.assertEqual(self.source.trn_type, 'do_cancel')
        self.assertEqual(self.source.trn_liveid, liveid)
        self.assert_(self.source.cancel_res_called)
        self.assertEqual(self.source.can_sessionid, sessionid)
        self.assertEqual(self.source.can_liveid, liveid)
        self.assertEqual(self.source.can_vid, vehicleid)
        self.assertEqual(self.source.can_start, start_time)
        self.assertEqual(self.source.can_end, end_time)
        self.assert_(self.source.res_builder_called)
        self.assertEqual(self.source.bld_logid, 'logid')
        self.assertEqual(self.source.bld_liveid, liveid)
        self.assertEqual(self.source.bld_modname, 'model name')
        self.assertEqual(self.source.bld_podname, 'pod name')
        self.assertEqual(reservation, 'my reservation')
    
    def testShouldDecodeLiveIdFromScriptWithPaymentKeysWell(self):
        code = r'''my_reservations.php?mv_action=confirm&_r=3&pk=149449011&payment_pk=149449017'''
        
        liveid = \
            self.source.decoder.decode_reservation_liveid_from_redirect_script_code(code)
        
        self.assertEqual(liveid, '149449011')

class ReservationsJsonHandlerTest (unittest.TestCase):
    def testShouldUseScreenscrapeFetchersAndJsonRenderers(self):
        handler = ReservationsJsonHandler()
        
        self.assertEqual(handler.error_view.__class__.__name__, 
            'ErrorJsonView')
        self.assertEqual(handler.reservation_source.__class__.__name__,
            'ReservationsScreenscrapeSource')
        self.assertEqual(handler.reservation_view.__class__.__name__,
            'ReservationsJsonView')

class ReservationJsonHandlerTest (unittest.TestCase):
    def testShouldUseScreenscrapeFetchersAndJsonRenderers(self):
        handler = ReservationJsonHandler()
        
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
        res1.logid = 'res1'
        res1.start_time = datetime.datetime(2010, 11, 15, 16, 30, tzinfo=Eastern)
        res1.end_time = datetime.datetime(2010, 11, 15, 17, 15, tzinfo=Eastern)
        res1.vehicle = StubObject()
        res1.vehicle.id = 'v123'
        res1.vehicle.model = StubObject()
        res1.vehicle.model.name = 'model 1'
        res1.vehicle.pod = StubObject()
        res1.vehicle.pod.id = 'pod123'
        res1.vehicle.pod.name = 'pod 1'
        res1.price = StubObject()
        res1.price.total_amount = 10.27
        
        res2 = StubObject()
        res2.logid = 'res2'
        res2.liveid = 'confid2'
        res2.start_time = datetime.datetime(2010, 12, 30, 16, 30, tzinfo=Eastern)
        res2.end_time = datetime.datetime(2010, 12, 31, 17, 15, tzinfo=Eastern)
        res2.vehicle = StubObject()
        res2.vehicle.id = 'v123'
        res2.vehicle.model = StubObject()
        res2.vehicle.model.name = 'model 1'
        res2.vehicle.pod = StubObject()
        res2.vehicle.pod.id = 'pod123'
        res2.vehicle.pod.name = 'pod 1'
        res2.price = StubObject()
        res2.price.total_amount = 10.39
        
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
        "logid": "res1", 
        "price": {
          "total_amount": 10.27
        }, 
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
        "liveid": "confid2", 
        "logid": "res2", 
        "price": {
          "total_amount": 10.39
        }, 
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
    
    def testShouldPrepareLoggedReservationForJsonDump(self):
        renderer = ReservationsJsonView()
        
        class StubObject (object):
            pass
        
        res1 = StubObject()
        res1.logid = 'res1'
        res1.start_time = datetime.datetime(2010, 11, 15, 16, 30, tzinfo=Eastern)
        res1.end_time = datetime.datetime(2010, 11, 15, 17, 15, tzinfo=Eastern)
        res1.vehicle = StubObject()
        res1.vehicle.id = 'v123'
        res1.vehicle.model = StubObject()
        res1.vehicle.model.name = 'model 1'
        res1.vehicle.pod = StubObject()
        res1.vehicle.pod.id = 'pod123'
        res1.vehicle.pod.name = 'pod 1'
        res1.price = StubObject()
        res1.price.total_amount = 4.12
        
        res_data = renderer.format_res_data(res1)
        self.assertEqual(res_data, {
            'logid' : 'res1',
            'start_time' : '2010-11-15T16:30',
            'end_time' : '2010-11-15T17:15',
            'vehicle' : {
                'id' : 'v123',
                'model' : {
                    'name' : 'model 1',
                },
                'pod' : {
                    'id' : 'pod123',
                    'name' : 'pod 1'
                }
            },
            'price' : {
                'total_amount' : 4.12
            }
        })
    
    def testShouldPrepareLiveReservationForJsonDump(self):
        renderer = ReservationsJsonView()
        
        class StubObject (object):
            pass
        
        res1 = StubObject()
        res1.logid = 'res1'
        res1.liveid = 'live1'
        res1.start_time = datetime.datetime(2010, 11, 15, 16, 30, tzinfo=Eastern)
        res1.end_time = datetime.datetime(2010, 11, 15, 17, 15, tzinfo=Eastern)
        res1.vehicle = StubObject()
        res1.vehicle.id = 'v123'
        res1.vehicle.model = StubObject()
        res1.vehicle.model.name = 'model 1'
        res1.vehicle.pod = StubObject()
        res1.vehicle.pod.id = 'pod123'
        res1.vehicle.pod.name = 'pod 1'
        res1.price = StubObject()
        res1.price.total_amount = 2.13
        
        res_data = renderer.format_res_data(res1)
        self.assertEqual(res_data, {
            'liveid' : 'live1',
            'logid' : 'res1',
            'start_time' : '2010-11-15T16:30',
            'end_time' : '2010-11-15T17:15',
            'vehicle' : {
                'id' : 'v123',
                'model' : {
                    'name' : 'model 1',
                },
                'pod' : {
                    'id' : 'pod123',
                    'name' : 'pod 1'
                }
            },
            'price' : {
                'total_amount': 2.13
            }
        })
    
    def testShouldRenderConfirmationJson(self):
        renderer = ReservationsJsonView()
        
        class StubObject (object):
            pass
        
        res1 = StubObject()
        res1.logid = 'res1'
        res1.start_time = datetime.datetime(2010, 11, 15, 16, 30, tzinfo=Eastern)
        res1.end_time = datetime.datetime(2010, 11, 15, 17, 15, tzinfo=Eastern)
        res1.vehicle = StubObject()
        res1.vehicle.id = 'v123'
        res1.vehicle.model = StubObject()
        res1.vehicle.model.name = 'model 1'
        res1.vehicle.pod = StubObject()
        res1.vehicle.pod.id = 'pod123'
        res1.vehicle.pod.name = 'pod 1'
        res1.price = StubObject()
        res1.price.total_amount = 11.82
        
        result = renderer.render_confirmation(None, res1, 'create')
        expected = \
"""{
  "confirmation": {
    "event": "create", 
    "reservation": {
      "end_time": "2010-11-15T17:15", 
      "logid": "res1", 
      "price": {
        "total_amount": 11.82
      }, 
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
    }
  }
}"""
        self.assertEqual(result, expected)

