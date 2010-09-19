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
        def get_reservations(self, sessionid, year_month=None):
            self.sessionid = sessionid
            self.year_month = year_month
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
        self.assertEqual(self.reservation_source.year_month, None)
        self.assertEqual(self.reservation_view.session, 'my session')
        self.assertEqual(self.reservation_view.reservations, 'my reservations')
        self.assertEqual(response, 'my reservation response')
    
    def testShouldCallGetReservationsHandler(self):
        @patch(self.handler)
        def handle_get_reservations(self):
            self.get_handler_called = True
        
        self.handler.get()
        
        self.assert_(self.handler.get_handler_called)

class ReservationsHtmlHandlerTest (unittest.TestCase):
    def testShouldBeIntializedWithScreenscrapeSourcesAndHtmlViews(self):
        handler = ReservationsHtmlHandler()
        self.assertEqual(handler.session_source.__class__.__name__,
                         'SessionScreenscrapeSource')
        self.assertEqual(handler.reservation_source.__class__.__name__,
                         'ReservationsScreenscrapeSource')
        self.assertEqual(handler.reservation_view.__class__.__name__,
                         'ReservationsHtmlView')
        self.assertEqual(handler.error_view.__class__.__name__,
                         'ErrorHtmlView')

class ReservationsScreenscrapeSourceTest (unittest.TestCase):
    def setUp(self):
        self.source = ReservationsScreenscrapeSource()
    
    def testShouldCreateAPcsConnection(self):
        conn = self.source.get_pcs_connection()
        self.assertEqual(conn.__class__.__name__, 'PcsConnection')
    
    def testShouldReturnUpcomingBodyAndHeadFromPcsConnection(self):
        @Stub(PcsConnection)
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
        @Stub(PcsConnection)
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
        
        conn = StubConnection()
        sessionid = 'ses1234'
        
        body, head = self.source.past_reservations_from_pcs(conn, sessionid, 2010, 10)
        
        self.assertEqual(conn.url, 'http://reservations.phillycarshare.org/my_reservations.php?mv_action=main&main[multi_filter][history][yearmonth]=201010')
        self.assertEqual(conn.method, 'GET')
        self.assertEqual(conn.data, {})
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my headers')
    
    NO_UPCOMING_RESERVATIONS_BODY = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_44_0_3" title="pcs_skin" media="screen, print" /></head>
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_44_0_3"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=12"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=12&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=12"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=12"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=12"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=12"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=12"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  >
  <option value="-1" selected>Current Reservations</option>
  <option value="201009">September&nbsp;2010</option>
  <option value="201008">August&nbsp;2010</option>
  <option value="201007">July&nbsp;2010</option>
  <option value="201006">June&nbsp;2010</option>
  <option value="201005">May&nbsp;2010</option>
  <option value="201004">April&nbsp;2010</option>
  <option value="201003">March&nbsp;2010</option>
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/>
<input type="hidden" name="_r" value="12"/>
<button  id="main" type="submit" class="button_update" ></button>
</td>
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><div class="dlist_empty"><span class="dlist_empty">The query did not return any results.</span></div></form></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_44_0_3"></script>
</body></html>'''
    def testShouldReturnEmptyReservationsListWhenNoUpcomingReservationsBodyReturnedFromPcs(self):
        html_data = BeautifulSoup(self.NO_UPCOMING_RESERVATIONS_BODY)
        reservations = self.source.get_reservation_data_from_html_data(html_data)
        
        self.assertEqual(len(reservations), 0)
    
    ONE_UPCOMING_RESERVATION = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_44_0_3" title="pcs_skin" media="screen, print" /></head>
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_44_0_3"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=26"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=26&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=26"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=26"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=26"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=26"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=26"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  >
  <option value="-1" selected>Current Reservations</option>
  <option value="201009">September&nbsp;2010</option>
  <option value="201008">August&nbsp;2010</option>
  <option value="201007">July&nbsp;2010</option>
  <option value="201006">June&nbsp;2010</option>
  <option value="201005">May&nbsp;2010</option>
  <option value="201004">April&nbsp;2010</option>
  <option value="201003">March&nbsp;2010</option>
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/>
<input type="hidden" name="_r" value="26"/>
<button  id="main" type="submit" class="button_update" ></button>
</td>
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td>
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=26&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td>
<td align="center"><font class="textbb">&nbsp;</font></td>
</tr></thead><tbody ><tr class="zebra"><td >2472498</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=26&pk=30005"    >47th & Baltimore - Prius Liftback</a></td>
<td >6:00 am Wednesday, September 15, 2010</td><td >6:15 am Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a>
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td width="176"><button  id="edit" type="button" class="button button_edit" onclick="; window.location='my_reservations.php?mv_action=edit&_r=26&pk=146299013'">Change</button>
<button  id="do_cancel" type="button" class="button button_do_cancel" onclick="; window.location='my_reservations.php?mv_action=do_cancel&_r=26&pk=146299013'">Cancel</button>
</td></tr></tbody></table></td></tr></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="mv_action" value="export_reservations"/>
<input type="hidden" name="_r" value="26"/>
<button  id="export_reservations" type="submit" class="button button_export" ></button>
</td>
</td></tr></table></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_44_0_3"></script>
</body></html>'''
    def testShouldReturnOneUpcomingReservationInAppropriateSituation(self):
        html_data = BeautifulSoup(self.ONE_UPCOMING_RESERVATION)
        reservations = self.source.get_reservation_data_from_html_data(html_data)
        
        self.assertEqual(len(reservations), 1)
        reservation = reservations[0]
        self.assertEqual(reservation.id, '2472498')
        self.assertEqual(reservation.start_time, datetime.datetime(2010,9,15,6,0,tzinfo=Eastern))
        self.assertEqual(reservation.price.total_amount, 3.24)
        self.assertEqual(reservation.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(reservation.vehicle.pod.name, '47th & Baltimore')
    
    ONE_CURRENT_ONE_UPCOMING_RESERVATIONS = r'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
<meta http-equiv="pragma" content="no-cache" />
<meta http-equiv="cache-control" content="no-cache" />
<title >Reservation Manager</title><link rel="stylesheet" type="text/css" href="/skin/pcs_ui.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_layout.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_buttons.css_3_44_0_3" title="pcs_skin" media="screen, print" /><link rel="stylesheet" type="text/css" href="/skin/pcs_skin.css_3_44_0_3" title="pcs_skin" media="screen, print" /></head>
<body bgcolor="white"  ><script language="javascript" type="text/javascript" src="/js/helper.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/prototype.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lowpro.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/slider.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mf_lightbox.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_base.js_3_44_0_3"></script>
<script language="javascript" type="text/javascript" src="/js/mv_reserve.js_3_44_0_3"></script>
<div class="mv_header">
<img border="0" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
</div>
<div id="wrapper"><div id="page_header"><div id="lame_image"><span class="switch">
<a class="text" href="/members/help.html?_r=35"  target="_blank"  >Help</a></span>
<p >Mjumbe Poe, you are signed in. (Residential Account)</p><a href="my_reservations.php?_r=35&mv_action=logout">
                            <img class="logbutton" alt = "Log Out" src="/skin/base_images/btn_logout.gif" />
                   </a></div><img id="logo" src="/images/client_images/pcs_web_logo.gif" alt="PhillyCarShare" title="PhillyCarShare" />
        <div id="nav_bar">
        <div id="navcontainer">
        <ul id="navlist"><li ><a class="text link_new_reservation" href="my_reservations.php?_r=35"    >New Reservation</a></li><li ><a class="link_my_reservations" href="my_reservations.php?mv_action=main&_r=35"    >My Reservations</a></li><li ><a class="text link_my_messages" href="my_messages.php?_r=35"    >My Messages</a></li><li ><a class="text link_my_info" href="my_info.php?_r=35"    >My Account</a></li><li ><a class="text link_my_problems" href="my_problems.php?_r=35"    >Member Feedback</a></li></ul></div></div></div><div class="midbox"><h3 >My Reservations</h3><h5 >Past and Current Reservations</h5><div class="multi_filter"><form id="main_multi_filter_" name="multi_filter" action="my_reservations.php" method="get"  ><label for="main_multi_filter__history_" id="main_multi_filter__history__label"><b>Reservation&nbsp;Selection</b>:&nbsp;</label><select name="main[multi_filter][history][yearmonth]"    id="main_multi_filter__history__yearmonth_" tabindex="0"  >
  <option value="-1" selected>Current Reservations</option>
  <option value="201009">September&nbsp;2010</option>
  <option value="201008">August&nbsp;2010</option>
  <option value="201007">July&nbsp;2010</option>
  <option value="201006">June&nbsp;2010</option>
  <option value="201005">May&nbsp;2010</option>
  <option value="201004">April&nbsp;2010</option>
  <option value="201003">March&nbsp;2010</option>
 </select><span class="instruction">&nbsp;</span><span ><td    align="center" valign="middle"  ><input type="hidden" name="mv_action" value="main"/>
<input type="hidden" name="_r" value="35"/>
<button  id="main" type="submit" class="button_update" ></button>
</td>
</span><input id="main_multi_filter__driver_pk_" type="hidden" name="main[multi_filter][driver_pk]" value="6285517" /></form></div><form name="main" method="post"><form id="main_dlist_" name="dlist" action="my_reservations.php" method="post"  ><tr ><td ><table class="dlist ma" id="main_dlist_"><thead ><tr ><td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_id&main[dlist][sort_dir]=asc"    >ID</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=ustack_descr&main[dlist][sort_dir]=asc"    >Stack</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_start&main[dlist][sort_dir]=asc"    >Start</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_end&main[dlist][sort_dir]=desc"    >End</a></td>
<th  width="1%"  align="center" valign="middle"  ><font class="textbb">Est&nbsp;Cost</font></th>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=reservation_status&main[dlist][sort_dir]=asc"    >Status</a></td>
<td     align="center" valign="middle"  ><a class="text" href="my_reservations.php?mv_action=main&_r=35&main[dlist][sort_col]=res_extra&main[dlist][sort_dir]=asc"    >Memo</a></td>
<td align="center"><font class="textbb">&nbsp;</font></td>
</tr></thead><tbody ><tr class="zebra"><td >2472500</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=35&pk=30005"    >47th & Baltimore - Prius Liftback</a></td>
<td >12:45 am Wednesday, September 15, 2010</td><td >1:00 am Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a>
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >TESTING CURRENT</td><td width="176"><button  id="early" type="button" class="button button_early" onclick="; window.location='my_reservations.php?mv_action=early&_r=35&pk=146299030'">Return Early</button>
<button  id="extend" type="button" class="button button_extend" onclick="; window.location='my_reservations.php?mv_action=extend&_r=35&pk=146299030'">Extend</button>
</td></tr><tr ><td >2472498</td><td   width="25%"  align="center" valign="middle"  ><a class="text" href="my_fleet.php?mv_action=show&_r=35&pk=30005"    >47th & Baltimore - Prius Liftback</a></td>
<td >6:00 am Wednesday, September 15, 2010</td><td >6:15 am Wednesday, September 15, 2010</td><td ><a href="#" class="tooltip_target" style="cursor: help;">$3.24</a>
                <span class="tooltip" style="position: absolute; z-index: 1000; display: none;">$0.63&nbsp;(Time)&nbsp;+<br/>$0.50&nbsp;(Distance&nbsp;@&nbsp;2&nbsp;mile(s))&nbsp;+<br/>$0.00&nbsp;(Fees)&nbsp;+<br/>$2.11&nbsp;(Tax)</span></td><td >Normal</td><td >&nbsp;</td><td width="176"><button  id="edit" type="button" class="button button_edit" onclick="; window.location='my_reservations.php?mv_action=edit&_r=35&pk=146299013'">Change</button>
<button  id="do_cancel" type="button" class="button button_do_cancel" onclick="; window.location='my_reservations.php?mv_action=do_cancel&_r=35&pk=146299013'">Cancel</button>
</td></tr></tbody></table></td></tr></form></form><form action="my_reservations.php" method="post"><table class="full_width"><tr ><td ><td    align="right" valign="middle"  ><input type="hidden" name="mv_action" value="export_reservations"/>
<input type="hidden" name="_r" value="35"/>
<button  id="export_reservations" type="submit" class="button button_export" ></button>
</td>
</td></tr></table></form></div><br style="clear: both" /><div id="mv_powered"><div id="mv_powered_left"><a href="http://www.metavera.com"><img src="/skin/base_images/mv_logo_small.gif" alt="Powered by Metavera"/></a></div><div id="mv_powered_right"><a href="http://www.metavera.com"><span>Powered by Metavera</span><br/>CarSharing Technology Leader</a></div></div></div><script language="javascript" type="text/javascript" src="/js/browser.js_3_44_0_3"></script>
</body></html>'''
    def testShouldtTwoReservationsInAppropriateSituation(self):
        html_data = BeautifulSoup(self.ONE_CURRENT_ONE_UPCOMING_RESERVATIONS)
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
        
        sessionid = 'ses1234'
        driverid = 'drv1234'
        
        reservations = self.source.get_reservations(sessionid)
        
        self.assert_(self.source.pcs_conn_called)
        self.assert_(self.source.upcoming_res_called)
        self.assert_(not self.source.past_res_called)
        self.assertEqual(self.source.conn, 'my connection')
        self.assertEqual(self.source.sessionid, 'ses1234')
        self.assertEqual(self.source.html_body, 'my body')
        self.assertEqual(self.source.html_doc, 'my html doc')
        self.assertEqual(reservations, 'my reservations')
    
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
        
        sessionid = 'ses1234'
        driverid = 'drv1234'
        
        reservations = self.source.get_reservations(sessionid, (2010, 11))
        
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

