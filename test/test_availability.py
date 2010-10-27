import unittest
import datetime
import new

from pcs.wsgi_handlers.wsgi import WsgiParameterError
from pcs.wsgi_handlers.wsgi.availability import VehicleAvailabilityHandler
from pcs.wsgi_handlers.wsgi.availability import LocationAvailabilityHandler
from pcs.wsgi_handlers.wsgi.availability import LocationAvailabilityHtmlHandler
from pcs.wsgi_handlers.wsgi.availability import LocationAvailabilityJsonHandler
from pcs.source import _AvailabilitySourceInterface
from pcs.source import _LocationsSourceInterface
from pcs.source import _SessionSourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
from pcs.source.screenscrape.pcsconnection import PcsConnection
from pcs.view import _AvailabilityViewInterface
from pcs.view import _ErrorViewInterface
from pcs.view.html.availability import AvailabilityHtmlView
from pcs.view.json.availability import AvailabilityJsonView
from util.testing import patch
from util.testing import Stub
from util.TimeZone import Eastern

class VehicleAvailabilityHandlerTest (unittest.TestCase):
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
        
        class StubAvailabilitySource (object):
            pass
        StubAvailabilitySource = Stub(_AvailabilitySourceInterface)(StubAvailabilitySource)
        
        class StubAvailabilityView (object):
            pass
        StubAvailabilityView = Stub(_AvailabilityViewInterface)(StubAvailabilityView)
        
        class StubErrorView (object):
            pass
        StubErrorView = Stub(_ErrorViewInterface)(StubErrorView)
        
        self.session_source = StubSessionSource()
        self.vehicle_source = StubAvailabilitySource()
        self.vehicle_view = StubAvailabilityView()
        self.error_view = StubErrorView()
        
        self.request = StubRequest()
        self.response = StubResponse()
    
    def testShouldUseCurrentTimeAndThreeHourDurationWhenNoStartOrEndIsGiven(self):
        # Given...
        handler = VehicleAvailabilityHandler(self.session_source, self.vehicle_source, 
                                 self.vehicle_view, self.error_view)
        handler.initialize(self.request, self.response)
        
        # When...
        start_time, end_time = handler.get_time_range()
        
        # Then...
        import datetime
        now_time = datetime.datetime.now(Eastern) + datetime.timedelta(minutes=1)
        later_time = now_time + datetime.timedelta(hours=3)
        threshold = datetime.timedelta(seconds=10)
        # ...can't check equality, as now_time and start_time were calculated at
        #    different times.  However, they should have been calculated within
        #    a certain amount of seconds from each other.
        self.assert_(-threshold < now_time - start_time < threshold, 
            "Time between (%s) and (%s) should be less than %s" % (now_time, start_time, threshold))
        self.assert_(-threshold < later_time - end_time < threshold,
            "Time between (%s) and (%s) should be less than %s" % (later_time, end_time, threshold))
    
    def testShouldPassCorrectVehicleIdToAvailabilitySourceForVehicleAvailability(self):
        # Given...
        self.request.cookies = { 'sid':'sid1234' }
        
        @patch(self.vehicle_source)
        def get_vehicle(self, sessionid, vehicleid, start_time, end_time):
            self.sessionid = sessionid
            self.vehicleid = vehicleid
            self.start_time = start_time
            self.end_time = end_time
            return 'My Availability'
        
        handler = VehicleAvailabilityHandler(self.session_source, self.vehicle_source, 
                                 self.vehicle_view, self.error_view)
        handler.initialize(self.request, self.response)
        
        # When...
        vehicleid = 'vid1234'
        sessionid = 'sid1234'
        start_time = 0
        end_time = 100
        vehicle = handler.get_vehicle(sessionid, vehicleid, start_time, end_time)
        
        # Then...
        self.assertEqual(self.vehicle_source.vehicleid, 'vid1234')
        self.assertEqual(self.vehicle_source.sessionid, 'sid1234')
        self.assertEqual(self.vehicle_source.start_time, 0)
        self.assertEqual(self.vehicle_source.end_time, 100)
        self.assertEqual(vehicle, 'My Availability')
    
    def testShouldPassCorrectVehicleIdAndTimeRangeToAvailabilitySourceForPriceEstimate(self):
        # Given...
        self.request['start_time'] = '2010-12-30T12:45'
        self.request['end_time'] = '2011-01-30T12:45'
        
        @patch(self.vehicle_source)
        def get_vehicle_price_estimate(self, sessionid, vehicleid, start_time, end_time):
            self.sessionid = sessionid
            self.vehicleid = vehicleid
            self.start_time = start_time
            self.end_time = end_time
            return 'My Availability'
        
        handler = VehicleAvailabilityHandler(self.session_source, self.vehicle_source, 
                                 self.vehicle_view, self.error_view)
        handler.initialize(self.request, self.response)
        
        # When...
        sessionid = 'sid1234'
        vehicleid = 'vid1234'
        start_time, end_time = handler.get_time_range()
        availability = handler.get_price_estimate(sessionid, vehicleid, start_time, end_time)
        
        # Then...
        self.assertEqual(self.vehicle_source.sessionid, 'sid1234')
        self.assertEqual(self.vehicle_source.vehicleid, 'vid1234')
        self.assertEqual(self.vehicle_source.start_time, datetime.datetime(2010, 12, 30, 12, 45, tzinfo=Eastern))
        self.assertEqual(self.vehicle_source.end_time, datetime.datetime(2011, 01, 30, 12, 45, tzinfo=Eastern))
        self.assertEqual(availability, 'My Availability')
        
    def testShouldRespondWithVehicleAvailabilityInformationBasedOnTheAvailabilitySource(self):
        handler = VehicleAvailabilityHandler(self.session_source, self.vehicle_source, 
                                 self.vehicle_view, self.error_view)
        handler.initialize(self.request, self.response)
        
        @patch(handler)
        def get_user_id(self):
            self.userid_called = True
            return 'user1234'
        
        @patch(handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(handler)
        def get_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
        
        @patch(handler)
        def get_vehicle(self, sessionid, vehicleid, start_time, end_time):
            self.vehicle_sessionid = sessionid
            self.vehicle_vehicleid = vehicleid
            self.vehicle_start_time = start_time
            self.vehicle_end_time = end_time
            return 'my vehicle'
        
        @patch(handler)
        def get_price_estimate(self, sessionid, vehicleid, start_time, end_time):
            self.price_sessionid = sessionid
            self.price_vehicleid = vehicleid
            self.price_start_time = start_time
            self.price_end_time = end_time
            return 'my price estimate'
        
        @patch(self.vehicle_view)
        def render_vehicle_availability(self, session, vehicle, start_time, end_time, price):
            self.session = session
            self.vehicle = vehicle
            self.start_time = start_time
            self.end_time = end_time
            return 'my vehicle info body'
        
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            return str(error_msg)
        
        handler.get('veh1234')
        
        self.assert_(handler.userid_called)
        self.assert_(handler.sessionid_called)
        self.assertEqual(handler.userid, 'user1234')
        self.assertEqual(handler.sessionid, 'ses1234')
        self.assertEqual(handler.vehicle_sessionid, 'ses1234')
        self.assertEqual(handler.vehicle_vehicleid, 'veh1234')
        self.assertEqual(handler.price_sessionid, 'ses1234')
        self.assertEqual(handler.price_vehicleid, 'veh1234')
#        self.assertEqual(self.vehicle_view.session, 'my session')
#        self.assertEqual(self.vehicle_view.vehicle, 'my vehicle')
        self.assertEqual(self.response.out.getvalue(), 'my vehicle info body')
        
    def testReturnContentFromErrorViewWhenAnExceptionIsRaised(self):
        handler = VehicleAvailabilityHandler(self.session_source, self.vehicle_source, 
                                 self.vehicle_view, self.error_view)
        handler.initialize(self.request, self.response)
        
        @patch(handler)
        def get_user_id(self):
            raise Exception('My Exception')
        
        @patch(handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(handler)
        def get_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
        
        @patch(handler)
        def get_vehicle(self, sessionid, vehicleid, start_time, end_time):
            self.vehicle_sessionid = sessionid
            self.vehicle_vehicleid = vehicleid
            self.vehicle_start_time = start_time
            self.vehicle_end_time = end_time
            return 'my vehicle'
        
        @patch(handler)
        def get_price_estimate(self, sessionid, vehicleid, start_time, end_time):
            self.price_sessionid = sessionid
            self.price_vehicleid = vehicleid
            self.price_start_time = start_time
            self.price_end_time = end_time
            return 'my price estimate'
        
        @patch(self.vehicle_view)
        def render_vehicle_availability(self, session, vehicle, start_time, end_time, price):
            self.session = session
            self.vehicle = vehicle
            self.start_time = start_time
            self.end_time = end_time
            return 'my vehicle info body'
        
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            return str(error_msg)
        
        handler.get('veh1234')
        
        response = handler.response.out.getvalue()
        self.assertEqual(response, "Exception: My Exception")
        

class VehicleAvailabilityHandlerAndScreenscrapeSourceTest (unittest.TestCase):
    
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
        
        class StubAvailabilitySource (object):
            pass
        StubAvailabilitySource = Stub(_AvailabilitySourceInterface)(StubAvailabilitySource)
        
        #class StubAvailabilityView (object):
        #    pass
        #StubAvailabilityView = Stub(_AvailabilityViewInterface)(StubAvailabilityView)
        
        class StubErrorView (object):
            pass
        StubErrorView = Stub(_ErrorViewInterface)(StubErrorView)
        
        self.session_source = StubSessionSource()
        #self.vehicle_source = StubAvailabilitySource()
        self.vehicle_view = StubAvailabilityView()
        self.error_view = StubErrorView()
        
        self.request = StubRequest()
        self.response = StubResponse()
    
class LocationAvailabilityHandlerTest (unittest.TestCase):
    
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
        
        # A source for session information
        class StubSessionSource (object):
            pass
        StubSessionSource = Stub(_SessionSourceInterface)(StubSessionSource)
        
        # A source for vehicle availability information
        class StubAvailabilitySource (object):
            pass
        StubAvailabilitySource = Stub(_AvailabilitySourceInterface)(StubAvailabilitySource)
        
        class StubLocationsSource (object):
            pass
        StubLocationsSource = Stub(_LocationsSourceInterface)(StubLocationsSource)
        
        # A generator for a representation (view) of the availability information
        class StubAvailabilityView (object):
            pass
        StubAvailabilityView = Stub(_AvailabilityViewInterface)(StubAvailabilityView)
        
        class StubErrorView (object):
            pass
        StubErrorView = Stub(_ErrorViewInterface)(StubErrorView)
        
        # The system under test
        self.session_source = StubSessionSource()
        self.vehicle_source = StubAvailabilitySource()
        self.location_source = StubLocationsSource()
        self.vehicle_view = StubAvailabilityView()
        self.error_view = StubErrorView()
        
        self.handler = LocationAvailabilityHandler(session_source=self.session_source, 
            vehicle_source=self.vehicle_source,
            location_source=self.location_source,
            vehicle_view=self.vehicle_view,
            error_view=self.error_view)
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
    
    def testShouldReturnSessionBasedOnReceivedCookies(self):
        # Given...
        self.handler.request.cookies = {'session':r'"{\"id\":\"ses1234\"}"'}
        
        # When...
        sessionid = self.handler.get_session_id()
        
        # Then...
        self.assertEqual(sessionid, 'ses1234')
    
    def testShouldReturnSessionBasedOnTheSessionSource(self):
        # Given...
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
        
        # When...
        session = self.handler.get_session('user1234', 'ses1234')
        
        # Then...
        self.assertEqual(session, 'my session')
        self.assertEqual(self.session_source.userid, 'user1234')
        self.assertEqual(self.session_source.sessionid, 'ses1234')
    
    def testShouldUseCurrentTimeAndThreeHourDurationWhenNoStartOrEndIsGiven(self):
        # Given...
        # ...(no explicit input state)
        
        # When...
        start_time, end_time = self.handler.get_time_range()
        
        # Then...
        import datetime
        now_time = datetime.datetime.now(Eastern) + datetime.timedelta(minutes=1)
        later_time = now_time + datetime.timedelta(hours=3)
        threshold = datetime.timedelta(seconds=10)
        # ...can't check equality, as now_time and start_time were calculated at
        #    different times.  However, they should have been calculated within
        #    a certain amount of seconds from each other.
        self.assert_(-threshold < now_time - start_time < threshold, 
            "Time between (%s) and (%s) should be less than %s" % (now_time, start_time, threshold))
        self.assert_(-threshold < later_time - end_time < threshold,
            "Time between (%s) and (%s) should be less than %s" % (later_time, end_time, threshold))
    
    def testShouldUseTimeBasedOnWhatIsPassedInToParametersWhenSupplied(self):
        # Given...
        self.handler.request['start_time'] = '2009-02-13T18:31:30' # 1234567890
        self.handler.request['end_time'] = '2009-02-13T19:21:30' # 1234570890
        
        # When...
        start_time, end_time = self.handler.get_time_range()
        
        # Then...
        from datetime import datetime as dt
        self.assertEqual(start_time, dt(2009, 2, 13, 18, 31, tzinfo=Eastern))
        self.assertEqual(end_time, dt(2009, 2, 13, 19, 21, tzinfo=Eastern))
    
    def testShouldGetSessionAndUserIdsFromCookies(self):
        # Given...
        self.handler.request.cookies = {
            'session':r'"{\"id\":\"123abc\",\"user\":\"u12345\",\"name\":\"\"}"'
        }
        
        # When...
        sessionid = self.handler.get_session_id()
        userid = self.handler.get_user_id()
        
        # Then...
        self.assertEqual(userid, 'u12345')
        self.assertEqual(sessionid, '123abc')
    
    def testMissingSessionIdRiasesError(self):
        # Given...
        self.handler.request.cookies = {
            'session':r'"{\"user\":\"u12345\"}"'
        }
        
        # When...
        try:
            sessionid = self.handler.get_session_id()
        
        # Then...
        except WsgiParameterError:
            return
        
        self.fail('Lack of session id should have caused a WsgiParameterError')
    
    def testMissingUserIdRiasesError(self):
        # Given...
        self.handler.request.cookies = {
            'session':r'"{\"sid\":\"123abc\"}"'
        }
        
        # When...
        try:
            userid = self.handler.get_user_id()
        
        # Then...
        except WsgiParameterError:
            return
        
        self.fail('Lack of session id should have caused a WsgiParameterError')
    
    def testShouldReturnAvailableVehiclesNearLocationBasedOnTheAvailabilitySource(self):
        # Given...
        @patch(self.vehicle_source)
        def get_available_vehicles_near(self, sessionid, locationid, start_time, end_time):
            self.sessionid = sessionid
            self.locationid = locationid
            self.start_time = start_time
            self.end_time = end_time
            return "vehicles"
        
        # When...
        sessionid = 'ses'
        locationid = 'loc'
        start_time, end_time = (1, 100)
        
        vehicles = self.handler.get_available_vehicles(sessionid, locationid, start_time, end_time)
        
        # Then...
        self.assertEqual(self.vehicle_source.sessionid, 'ses')
        self.assertEqual(self.vehicle_source.locationid, 'loc')
        self.assertEqual(self.vehicle_source.start_time, 1)
        self.assertEqual(self.vehicle_source.end_time, 100)
        self.assertEqual(vehicles, "vehicles")
    
    def testShouldReturnLocationIdBasedOnTheParametersSupplied(self):
        # Given...
        self.handler.request['location_id'] = 'loc1234'
        
        # When...
        locationid = self.handler.get_location_id()
        
        # Then...
        self.assertEqual(locationid, 'loc1234')
    
    def testShouldReturnLatitudeLogitudeTupleAsLocationIdWhenSupplied(self):
        # Given...
        self.handler.request['latitude'] = '123.4'
        self.handler.request['longitude'] = '567.8'
        
        # When...
        locationid = self.handler.get_location_id()
        
        # Then...
        self.assertEqual(locationid, (123.4,567.8))
    
    def testShouldRaiseAnErrorWhenNoLocationIdSupplied(self):
        # Given...
        # ...no parameters
        
        # When...
        try:
            locationid = self.handler.get_location_id()
        
        # Then...
        except WsgiParameterError:
            return
        
        self.fail('Should raise WsgiParameterError when no location id or log/lat supplied')
    
    def testShouldReturnLocationAccordingToLocationSourceWhenGivenALocationId(self):
        # Given...
        @patch(self.location_source)
        def get_location_profile(self, sessionid, locationid):
            self.sessionid = sessionid
            self.locationid = locationid
            return 'my location'
        
        # When...
        sessionid = 'ses1234'
        locationid = 'loc1234'
        location = self.handler.get_location(sessionid, locationid)
        
        # Then...
        self.assertEqual(self.location_source.sessionid, 'ses1234')
        self.assertEqual(self.location_source.locationid, 'loc1234')
        self.assertEqual(location, 'my location')
    
    def testShouldReturnLocationAccordingToLocationSourceWhenGivenALatitudeAndLongitude(self):
        # Given...
        @patch(self.location_source)
        def get_custom_location(self, location_name, location_key):
            self.location_name = location_name
            self.location_key = location_key
            return 'my location'
        
        # When...
        sessionid = 'ses1234'
        locationid = (123,456)
        location = self.handler.get_location(sessionid, locationid)
        
        # Then...
        self.assertEqual(self.location_source.location_name, 'My Current Location')
        self.assertEqual(self.location_source.location_key, (123,456))
        self.assertEqual(location, 'my location')
    
    def testShouldRespondWithFailureContentWhenSessionSourceCannotFindSessionWithGivenId(self):
        """With no valid session, the availability handler will give a failure document response."""
        
        # Given...
        @patch(self.handler)
        def get_user_id(self):
            raise Exception("Failure")
        
        @patch(self.handler)
        def get_session_id(self):
            raise Exception("Failure")
        
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            return error_msg
        
        # When...
        self.handler.get('loc1234')
        
        # Then...
        response = self.handler.response.out.getvalue()
        self.assertEqual(response, "Exception: Failure")
    
    def testGetMethodShouldInteractWithOtherMethodsWithSuccess(self):
        # Given...
        @patch(self.handler)
        def get_user_id(self):
            self.get_user_id_called = True
            return 'user1234'
        
        @patch(self.handler)
        def get_session_id(self):
            self.get_session_id_called = True
            return 'ses1234'
        
        @patch(self.handler)
        def get_location_id(self):
            self.get_location_id_called = True
            return 'loc1234'
        
        @patch(self.handler)
        def get_session(self, userid, sessionid):
            self.get_session_userid = userid
            self.get_session_sessionid = sessionid
            
            class Dummy (object): pass
            mysession = Dummy()
            mysession.id = sessionid
            return mysession
        
        @patch(self.handler)
        def get_location(self, sessionid, locationid):
            self.get_location_sessionid = sessionid
            self.get_location_locationid = locationid
            
            class Dummy (object): pass
            mylocation = Dummy()
            mylocation.id = locationid
            return mylocation
        
        @patch(self.handler)
        def get_time_range(self):
            return (1, 100)
        
        @patch(self.handler)
        def get_available_vehicles(self, sessionid, locationid, start_time, end_time):
            self.available_sessionid = sessionid
            self.available_locationid = locationid
            self.available_start = start_time
            self.available_end = end_time
            return ['v1','v2']
        
        @patch(self.vehicle_view)
        def render_location_availability(self, session, location, start_time, end_time, vehicle_availabilities):
            self.available_session = session
            self.available_location = location
            self.available_vehicles = vehicle_availabilities
            self.available_start = start_time
            self.available_end = end_time
            return 'Success'
        
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            return error_msg
        
        # When...
        self.handler.get('loc1234')
        response_body = self.handler.response.out.getvalue()
        
        # Then...
        self.assert_(self.handler.get_user_id_called)
        self.assert_(self.handler.get_session_id_called)
#        self.assert_(self.handler.get_location_id_called)
        self.assertEqual(self.handler.get_session_userid, 'user1234')
        self.assertEqual(self.handler.get_session_sessionid, 'ses1234')
        self.assertEqual(self.handler.get_location_sessionid, 'ses1234')
        self.assertEqual(self.handler.get_location_locationid, 'loc1234')
        self.assertEqual(self.vehicle_view.available_session.id, 'ses1234')
        self.assertEqual(self.vehicle_view.available_location.id, 'loc1234')
#        self.assertEqual(self.vehicle_view.available_start, 1)
#        self.assertEqual(self.vehicle_view.available_end, 100)
        self.assertEqual(response_body, 'Success')
    
    def testLocationIdOfZeroShouldBeValid(self):
        """Receiving a request with a location id of 0 should not raise an exception"""
        
        # Given...
        @patch(self.error_view)
        def render_error(self, error_code, error_msg, error_detail):
            return error_msg
        
        self.handler.request['start_time'] = 100
        self.handler.request['end_time'] = 10000
        self.handler.request['location_id'] = 0
        self.handler.request.cookies = {
          'sid':'5',
          'suser':'4600'
        }
        
        # ...and the session source recognizes the cookies:
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            class StubSession (object):
                id = 5
                user = '4600'
                name = "Jim Jacobsen"
            return StubSession()
        
        @patch(self.location_source)
        def get_location_profile(self, sessionid, locationid):
            class StubLocation (object):
                id = locationid
            return StubLocation()
        
        # When...
        try:
            self.handler.get(0)
        
        # Then...
        except WsgiParameterError:
            self.fail('No parameter exception should have been raised.')
        

class AvailabilityScreenscrapeSourceTest (unittest.TestCase):
    
    def setUp(self):
        self.source = AvailabilityScreenscrapeSource('res.pcs.org', '/vehicles.php?action=new', '/vehicle.php', '/price.php')
    
    def testCreateHostConnectionShouldReturnAPcsConnection(self):
        # When...
        conn = self.source.create_host_connection()
        
        # Then...
        self.assertEqual(conn.__class__.__name__, 'PcsConnection')
        
    def testShouldGetAvailabilityFromPcsBasedOnConnectionResponse(self):
        # Given...
        class StubResponse (object):
            def read(self):
                return 'my body'
            def getheaders(self):
                return 'my head'
        
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.url = url
                self.method = method
                self.data = data
                self.headers = headers
                return StubResponse()
        StubConnection = Stub(PcsConnection)(StubConnection)
        conn = StubConnection()
        
        sessionid = 'ses1234'
        locationid = 'loc1234'
        start_time = datetime.datetime(2010, 9, 4, 11, 15)
        end_time = datetime.datetime(2010, 9, 4, 13, 45)
        
        # When...
        body, head = self.source.availability_from_pcs(conn, sessionid, locationid, start_time, end_time)
        
        # Then...
        self.assertEqual(conn.url, 'http://res.pcs.org/vehicles.php?action=new&location=driver_locations_loc1234&start_date=9/4/2010&start_time=40500&end_date=9/4/2010&end_time=49500')
        self.assertEqual(conn.method, 'GET')
        self.assertEqual(conn.data, {})
        self.assertEqual(conn.headers, { 'Cookie':'sid=ses1234' })
        self.assertEqual(body, 'my body')
        self.assertEqual(head, 'my head')
    
    def testLocationQueryShouldUseLocationProfileIdForStringKey(self):
        # Given...
        locationid = 'loc1234'
        
        # When...
        query = self.source.get_location_query(locationid)
        
        # Then...
        self.assertEqual(query, 'location=driver_locations_loc1234')
    
    def testLocationQueryShouldUseLocationProfileIdForLatitudeLongitudePair(self):
        # Given...
        location_coord = (123.4,567.8)
        
        # When...
        query = self.source.get_location_query(location_coord)
        
        # Then...
        self.assertEqual(query, 'location_latitude=123.4&location_longitude=567.8')
    
    def testTimeQueryShouldUseStartAndEndTimeGiven(self):
        # Given...
        start_time = datetime.datetime(2010, 10, 4, 11, 15)
        end_time = datetime.datetime(2012, 9, 5, 13, 45)
        
        # When...
        query = self.source.get_time_query(start_time, end_time)
        
        # Then...
        self.assertEqual(query, 'start_date=10/4/2010&start_time=40500&end_date=9/5/2012&end_time=49500')
    
    def testShouldLoadAppropriateJsonObjectFromString(self):
        # Given...
        json_string = r'{"pods":["<div class=\"pod_top\"></div>","<div class=\"pod_bottom\"></div>"]}'
        
        # When...
        json_data = self.source.get_json_data(json_string)
        
        # Then...
        self.assertEqual(json_data,
            {'pods':['<div class="pod_top"></div>','<div class="pod_bottom"></div>']})
    
    def testShouldLoadAppropriateHtmlDocumentObjectFromPodsFieldOfJsonObject(self):
        """Should load appropriate HTML document object from the 'pods' field of the JSON object"""
        # Given...
        json_data = {'pods':['<div class="pod_top"></div><div class="pod_bottom"></div>','<div class="pod_top"></div><div class="pod_bottom"></div><div class="pod_bottom"></div>']}
        
        # When...
        html_data = self.source.get_html_data(json_data)
        
        # Then...
        all_divs = html_data.findAll('div')
        btm_divs = html_data.findAll('div', {'class':'pod_bottom'})
        
        self.assertEqual(len(all_divs), 5)
        self.assertEqual(len(btm_divs), 3)
    
    def testShouldCreateCorrectPodFromHtmlData(self):
        # Given...
        doc_string = r'''<html><body><div class="pod_top"><div class="pod_head"><h4><a class="text" href="my_fleet.php?mv_action=show&amp;_r=8&amp;pk=30005" onclick="MV.controls.results.show_pod_details(30005); return false;">47th &amp; Baltimore - 0.08 mile(s)</a></h4></div></div><div class="pod_top"><div class="pod_head"><h4><a class="text" href="my_fleet.php?mv_action=show&amp;_r=8&amp;pk=12174212" onclick="MV.controls.results.show_pod_details(12174212); return false;">46th &amp; Baltimore - 0.2 mile(s)</a></h4></div></div></body></html>'''
        from util.BeautifulSoup import BeautifulSoup
        doc = BeautifulSoup(doc_string)
        pod_info_divs = doc.findAll('div', {'class': 'pod_top'})
        pod_info_div = pod_info_divs[0]
        
        # When...
        pod, dist = self.source.get_pod_and_distance_from_html_data(pod_info_div)
        
        # Then...
        self.assertEqual(pod.id, '30005')
        self.assertEqual(pod.name, '47th &amp; Baltimore')
        self.assertEqual(dist, 0.08)
    
    def testShouldCreateCorrectVehicleAvailabilityFromHtmlData(self):
        # Given...
        doc_string = r'''<html><body><div class="pod_bot pod_bot_maybe" id="page_result_1"><div id="time_line"><img width="439" height="25" src="skin/base_images/day_guage.gif"><span class="pod_estimates_images"><img src="/skin/base_images/hourly_cost.gif"></span></div><div class="list_left"><div class="v_img"><a href="http://www.phillycarshare.org/cars/prius" target="_blank"><img style="border: 0;" src="/images/client_images/prius_lift_thumb.gif"></a></div><div class="v_name"><h4>Prius Liftback</h4></div><div class="v_amenities"><ul><li><img src="/skin/base_images/hybrid.gif" label="Hybrid" title="Hybrid"></li><li><img src="/skin/base_images/folding_seat.gif" label="Folding Rear Seats" title="Folding Rear Seats"></li></ul></div></div><div class="list_mid"><div class="time"><ul class="segments"><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li><ul><li class="slct_bkd pad_end"></li><li class="slct_bkd"></li><li class="slct_bkd"></li><li class="slct_bkd pad_end"></li></ul></li><li><ul><li class="slct_bkd pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li><ul><li class="good pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li><li><ul><li class="free pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li></ul></div><div class="brick" style="width:50px; margin-left: 141px; -margin-left: 68px;"></div><div class="timestamp"><p class="maybe">Available from 3:15 pm on 08/24</p></div></div><div class="list_right"><div class="reserve"><a href="javascript:MV.controls.reserve.lightbox.create('1282672800', '1282683600', '96692246', '');">Select<span id="estimate_stack_956" class="est">$22.47</span></a></div><div id="rates_stack_956" class="price"><div><nobr><strong>$4.45</strong></nobr><br><nobr></nobr></div></div></div></div></body></html>'''
        from util.BeautifulSoup import BeautifulSoup
        doc = BeautifulSoup(doc_string)
        bodies = doc.findAll('body')
        body = bodies[0]
        vehicle_info_divs = body.findAll('div', recursive=False)
        vehicle_info_div = vehicle_info_divs[0]
        start_time = 100
        end_time = 1000
        
        fake_pod = object()
        
        # When...
        vehicle_availability = self.source.get_vehicle_from_html_data(fake_pod, vehicle_info_div, start_time, end_time)
        
        # Then...
        self.assertEqual(vehicle_availability.vehicle.model.name, 'Prius Liftback')
        self.assertEqual(vehicle_availability.vehicle.pod, fake_pod)
        self.assertEqual(vehicle_availability.vehicle.id, '96692246')
    
    def testShouldGetTheCorrectNumberOfAvailabilitiesSpecifiedOnPcsSite(self):
        # Given...
        class StubConnection (object):
            def request(self, url, method, data, headers):
                import StringIO
                class StubResponse (StringIO.StringIO):
                    def getheaders(self):
                        return {}
                return StubResponse('{"pods":[' +
                    ','.join([r'''"<div class=\"pod_top\"><div class=\"pod_head\"><h4 ><a class=\"text\" href=\"my_fleet.php?mv_action=show&_r=16&pk=30005\"   onclick=\"MV.controls.results.show_pod_details(30005); return false;\" >47th & Baltimore - 0.08 mile(s)</a></h4></div></div><div class=\"pod_bot \" id=\"page_result_1\"><div id=\"time_line\"><img width=\"439\" height=\"25\" src=\"skin/base_images/day_guage.gif\" /><span class=\"pod_estimates_images\"><img src=\"/skin/base_images/hourly_cost.gif\" /></span></div><div class=\"list_left\"><div class=\"v_img\"><a href=\"http://www.phillycarshare.org/cars/tacoma\" target=\"_blank\"><img style=\"border: 0;\" src=\"/images/client_images/toyota_tacoma_thumb.gif\"/></a></div><div class=\"v_name\"><h4>Tacoma Pickup</h4></div><div class=\"v_amenities\"><ul></ul></div></div><div class=\"list_mid\"><div class=\"time\"><ul class=\"segments\"><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li></ul></div><div class=\"brick\" style=\"width:32px; margin-left: 333px; -margin-left: 164px;\"></div><div class=\"timestamp\"><p class=\"good\">Available</p></div></div><div class=\"list_right\"><div class=\"reserve\"><a href=\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '91800598', '');\">Select<span id=\"estimate_stack_894\" class=\"est\"></span></a></div><div id=\"rates_stack_894\" class=\"price\"></div></div></div><div class=\"pod_bot \" id=\"page_result_2\"><div class=\"list_left\"><div class=\"v_img\"><img style=\"border: 0;\" src=\"/images/client_images/prius_lift_thumb.gif\"/></div><div class=\"v_name\"><h4>Prius Liftback</h4></div><div class=\"v_amenities\"><ul><li><img src=\"/skin/base_images/hybrid.gif\" label=\"Hybrid\" title=\"Hybrid\"/></li>n<li><img src=\"/skin/base_images/folding_seat.gif\" label=\"Folding Rear Seats\" title=\"Folding Rear Seats\"/></li></ul></div></div><div class=\"list_mid\"><div class=\"time\"><ul class=\"segments\"><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li></ul></div><div class=\"brick\" style=\"width:32px; margin-left: 333px; -margin-left: 164px;\"></div><div class=\"timestamp\"><p class=\"good\">Available</p></div></div><div class=\"list_right\"><div class=\"reserve\"><a href=\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '96692246', '');\">Select<span id=\"estimate_stack_956\" class=\"est\"></span></a></div><div id=\"rates_stack_956\" class=\"price\"></div></div></div>"''',
                              r'''"<div class=\"pod_top\"><div class=\"pod_head\"><h4 ><a class=\"text\" href=\"my_fleet.php?mv_action=show&_r=16&pk=12174212\"   onclick=\"MV.controls.results.show_pod_details(12174212); return false;\" >46th & Baltimore - 0.2 mile(s)</a></h4></div></div><div class=\"pod_bot \" id=\"page_result_3\"><div class=\"list_left\"><div class=\"v_img\"><a href=\"http://www.phillycarshare.org/cars/element\" target=\"_blank\"><img style=\"border: 0;\" src=\"/images/client_images/honda_element_thumb.gif\"/></a></div><div class=\"v_name\"><h4>Honda Element</h4></div><div class=\"v_amenities\"><ul><li><img src=\"/skin/base_images/awd.gif\" label=\"All Wheel Drive\" title=\"All Wheel Drive\"/></li>n<li><img src=\"/skin/base_images/folding_seat.gif\" label=\"Folding Rear Seats\" title=\"Folding Rear Seats\"/></li></ul></div></div><div class=\"list_mid\"><div class=\"time\"><ul class=\"segments\"><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li></ul></div><div class=\"brick\" style=\"width:32px; margin-left: 333px; -margin-left: 164px;\"></div><div class=\"timestamp\"><p class=\"good\">Available</p></div></div><div class=\"list_right\"><div class=\"reserve\"><a href=\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '130868710', '');\">Select<span id=\"estimate_stack_1195\" class=\"est\"></span></a></div><div id=\"rates_stack_1195\" class=\"price\"></div></div></div><div class=\"pod_bot \" id=\"page_result_4\"><div class=\"list_left\"><div class=\"v_img\"><img style=\"border: 0;\" src=\"/images/client_images/prius_lift_thumb.gif\"/></div><div class=\"v_name\"><h4>Prius Liftback</h4></div><div class=\"v_amenities\"><ul><li><img src=\"/skin/base_images/hybrid.gif\" label=\"Hybrid\" title=\"Hybrid\"/></li>n<li><img src=\"/skin/base_images/folding_seat.gif\" label=\"Folding Rear Seats\" title=\"Folding Rear Seats\"/></li></ul></div></div><div class=\"list_mid\"><div class=\"time\"><ul class=\"segments\"><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"bad pad_end\" /></ul></li><li ><ul ><li class=\"bad pad_end\" /><li class=\"bad\" /><li class=\"bad\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"good\" /><li class=\"good\" /><li class=\"good pad_end\" /></ul></li><li ><ul ><li class=\"good pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li><li ><ul ><li class=\"free pad_end\" /><li class=\"free\" /><li class=\"free\" /><li class=\"free pad_end\" /></ul></li></ul></div><div class=\"brick\" style=\"width:32px; margin-left: 333px; -margin-left: 164px;\"></div><div class=\"timestamp\"><p class=\"good\">Available</p></div></div><div class=\"list_right\"><div class=\"reserve\"><a href=\"javascript:MV.controls.reserve.lightbox.create('1282540500', '1282547700', '73484842', '');\">Select<span id=\"estimate_stack_734\" class=\"est\"></span></a></div><div id=\"rates_stack_734\" class=\"price\"></div></div></div>"''']) + 
                    ']}')
        StubConnection = Stub(PcsConnection)(StubConnection)
        
        sessionid = ''
        locationid = ''
        stime = etime = datetime.datetime.now(Eastern)
        
        @patch(self.source)
        def create_host_connection(self):
            return StubConnection()
        
        # When...
        vehicle_availabilities = self.source.get_available_vehicles_near(sessionid,locationid,stime,etime)
        
        # Then...
        self.assertEqual([va.vehicle.model.name for va in vehicle_availabilities], ['Tacoma Pickup','Prius Liftback','Honda Element','Prius Liftback'])
    
    def testShouldCorrectlyParseAvailabilityFromStipulationAboutEarliestAvailability(self):
        source = AvailabilityScreenscrapeSource()
        class StubVehicle (object):
            pass
        vehicle = StubVehicle()
        stipulation = 'Available from 3:30 pm on 09/01'
        
        source.assign_vehicle_availability_stipulation(vehicle, stipulation)
        
        now = datetime.datetime.now(Eastern)
        year = now.year if now.month < 9 else now.year+1
        month = 9
        day = 1
        hour = 15
        minute = 30
        self.assertEqual(vehicle.earliest, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
    
    def testShouldCorrectlyParseAvailabilityFromStipulationAboutLatestAvailability(self):
        source = AvailabilityScreenscrapeSource()
        class StubVehicle (object):
            pass
        vehicle = StubVehicle()
        stipulation = 'Available until 3:30 pm on 09/01'
        
        source.assign_vehicle_availability_stipulation(vehicle, stipulation)
        
        now = datetime.datetime.now(Eastern)
        year = now.year if now.month < 9 else now.year+1
        month = 9
        day = 1
        hour = 15
        minute = 30
        self.assertEqual(vehicle.latest, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
    
    def testShouldCorrectlyParseAvailabilityFromStipulationAboutSandwichedAvailability(self):
        source = AvailabilityScreenscrapeSource()
        class StubVehicle (object):
            pass
        vehicle = StubVehicle()
        stipulation = 'Available from 3:30 pm on 09/01 to 4:45 am on 09/02'
        
        source.assign_vehicle_availability_stipulation(vehicle, stipulation)
        
        now = datetime.datetime.now(Eastern)
        year = now.year if now.month < 9 else now.year+1
        month = 9
        day = 1
        hour = 15
        minute = 30
        self.assertEqual(vehicle.earliest, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
        
        now = datetime.datetime.now(Eastern)
        day = 2
        hour = 4
        minute = 45
        self.assertEqual(vehicle.latest, datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern))
    
    def testConnectionShouldRespndWithCorrectVehicleAvailability(self):
        # Given...
        class StubResponse (object):
            def read(self):
                return 'my vehicle info body'
            def getheaders(self):
                return 'my head'
        
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.url = url
                self.method = method
                self.data = data
                self.headers = headers
                return StubResponse()
        StubConnection = Stub(PcsConnection)(StubConnection)
        conn = StubConnection()
        
        sessionid = 'ses1234'
        vehicleid = 'veh1234'
        start_time = datetime.datetime(2010, 9, 6, 2, 15, tzinfo=Eastern)
        end_time = datetime.datetime(2010, 9, 6, 5, 15, tzinfo=Eastern)
        
        # When...
        body, head = self.source.vehicle_info_from_pcs(conn, sessionid, vehicleid, start_time, end_time)
        
        # Then...
        self.assertEqual(conn.url, 'http://res.pcs.org/vehicle.php')
        self.assertEqual(conn.method, 'POST')
        self.assertEqual(conn.data, 'default%5Bend_stamp%5D=1283764500&mv_action=add&default%5Bstack_pk%5D=veh1234&default%5Bstart_stamp%5D=1283753700')
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
        self.assertEqual(body, 'my vehicle info body')
        self.assertEqual(head, 'my head')
    
    def testHtmlBodyTextShouldParseIntoExpectedHtmlDocument(self):
        # Given...
        html_body = r'''<div>Hello</div><script>alert("World");</script>'''
        
        # When...
        html_data = self.source.get_html_vehicle_data(html_body)
        
        # Then...
        self.assertEqual(html_data.find('body').find('div').text, 'Hello')
    
    def testHtmlBodyFromAvailabilityRequestShouldProduceExpectedVehicleAvailability(self):
        html_body = r'''<html><body><div class="lightbox" id="fakeLightbox"><h3 >Your Reservation</h3><div class="lightbox_contents"><p id="lightbox_instruction" class="error"></p><form class="reservation" id="add" name="add" method="post" action="lightbox.php"><div class="left_panel"><fieldset class="stack_fieldset"><input type="hidden" name="add[stack_pk]" value="91800598" /><table ><tr ><td ><label for="add_stack_pk__location">Location:</label></td><td ><span id="add_stack_pk__location">47th & Baltimore</span></td></tr><tr ><td ><label for="add_stack_pk_vt">Vehicle Type:</label></td><td ><span id="add_stack_pk_vt">Tacoma Pickup</span></td></tr></table></fieldset><fieldset class="range_fieldset"><table ><tr ><td ><label for="add_start_stamp__start_date_">Start:</label></td><td class="stamp_control"><input id="add_start_stamp__start_date_" name="add[start_stamp][start_date][date]" class="date_control" onchange="" value="09/06/10" />    <script language="javascript" type="text/javascript">
        DateInput('add_start_stamp__start_date__calendar', 'add_start_stamp__start_date_', true, '1283753498', 'm/d/y', null, null);
    </script><select id="add_start_stamp__start_time_" name="add[start_stamp][start_time][time]" class="time_control"><option value="0">Midnight</option><option value="900">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100" selected="selected">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800">03:00 AM</option><option value="11700">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_end_stamp__end_date_">End:</label></td><td class="stamp_control"><input id="add_end_stamp__end_date_" name="add[end_stamp][end_date][date]" class="date_control" onchange="" value="09/06/10" />    <script language="javascript" type="text/javascript">
        DateInput('add_end_stamp__end_date__calendar', 'add_end_stamp__end_date_', true, '1283753498', 'm/d/y', null, null);
    </script><select id="add_end_stamp__end_time_" name="add[end_stamp][end_time][time]" class="time_control"><option value="0">Midnight</option><option value="900">12:15 AM</option><option value="1800">12:30 AM</option><option value="2700">12:45 AM</option><option value="3600">01:00 AM</option><option value="4500">01:15 AM</option><option value="5400">01:30 AM</option><option value="6300">01:45 AM</option><option value="7200">02:00 AM</option><option value="8100">02:15 AM</option><option value="9000">02:30 AM</option><option value="9900">02:45 AM</option><option value="10800">03:00 AM</option><option value="11700">03:15 AM</option><option value="12600">03:30 AM</option><option value="13500">03:45 AM</option><option value="14400">04:00 AM</option><option value="15300">04:15 AM</option><option value="16200">04:30 AM</option><option value="17100">04:45 AM</option><option value="18000">05:00 AM</option><option value="18900" selected="selected">05:15 AM</option><option value="19800">05:30 AM</option><option value="20700">05:45 AM</option><option value="21600">06:00 AM</option><option value="22500">06:15 AM</option><option value="23400">06:30 AM</option><option value="24300">06:45 AM</option><option value="25200">07:00 AM</option><option value="26100">07:15 AM</option><option value="27000">07:30 AM</option><option value="27900">07:45 AM</option><option value="28800">08:00 AM</option><option value="29700">08:15 AM</option><option value="30600">08:30 AM</option><option value="31500">08:45 AM</option><option value="32400">09:00 AM</option><option value="33300">09:15 AM</option><option value="34200">09:30 AM</option><option value="35100">09:45 AM</option><option value="36000">10:00 AM</option><option value="36900">10:15 AM</option><option value="37800">10:30 AM</option><option value="38700">10:45 AM</option><option value="39600">11:00 AM</option><option value="40500">11:15 AM</option><option value="41400">11:30 AM</option><option value="42300">11:45 AM</option><option value="-1"></option><option value="43200">Noon</option><option value="44100">12:15 PM</option><option value="45000">12:30 PM</option><option value="45900">12:45 PM</option><option value="46800">01:00 PM</option><option value="47700">01:15 PM</option><option value="48600">01:30 PM</option><option value="49500">01:45 PM</option><option value="50400">02:00 PM</option><option value="51300">02:15 PM</option><option value="52200">02:30 PM</option><option value="53100">02:45 PM</option><option value="54000">03:00 PM</option><option value="54900">03:15 PM</option><option value="55800">03:30 PM</option><option value="56700">03:45 PM</option><option value="57600">04:00 PM</option><option value="58500">04:15 PM</option><option value="59400">04:30 PM</option><option value="60300">04:45 PM</option><option value="61200">05:00 PM</option><option value="62100">05:15 PM</option><option value="63000">05:30 PM</option><option value="63900">05:45 PM</option><option value="64800">06:00 PM</option><option value="65700">06:15 PM</option><option value="66600">06:30 PM</option><option value="67500">06:45 PM</option><option value="68400">07:00 PM</option><option value="69300">07:15 PM</option><option value="70200">07:30 PM</option><option value="71100">07:45 PM</option><option value="72000">08:00 PM</option><option value="72900">08:15 PM</option><option value="73800">08:30 PM</option><option value="74700">08:45 PM</option><option value="75600">09:00 PM</option><option value="76500">09:15 PM</option><option value="77400">09:30 PM</option><option value="78300">09:45 PM</option><option value="79200">10:00 PM</option><option value="80100">10:15 PM</option><option value="81000">10:30 PM</option><option value="81900">10:45 PM</option><option value="82800">11:00 PM</option><option value="83700">11:15 PM</option><option value="84600">11:30 PM</option><option value="85500">11:45 PM</option></select></td></tr><tr ><td ><label for="add_job_code_">Memo:</label></td><td ><input id="add_job_code_" name="add[job_code]" type="text" size="25" maxlength="25" value="" onkeypress="
            var keyCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
                if (keyCode == 13) {
                    return false;
                }
                return true;
        " class="memo_control" /></td></tr><tr ><td colspan="2" style="color: #f50c0c; font-size: 11px; font-weight: bold;">Consider padding your time. Returning after your reservation End Time will cost you $40 per half hour.</td></tr></table><input id="add_tid_" type="hidden" name="add[tid]" value="3"/>
<input type="hidden" name="mv_action" value="add" /><input type="hidden" name="_r" value="7" /></fieldset></div><div class="right_panel"><img class="vehicle" src="/images/client_images/toyota_tacoma.jpg" alt="Tacoma Pickup" /><div class="price"><div id="add_price__price_" class="container">$??.00 hourly / $??.00 daily</div></div><ul class="amenity"><li ></li></ul></div><div class="bottom_panel"><div class="cost"><div id="add_balance__balance__div"><label for="add_balance__balance_">AVAILABLE BALANCE:</label><span id="add_balance__balance_" class=""></span></div></div><div class="cost"><label for="add_estimate__estimate_">ESTIMATED COST:</label><span id="add_estimate__estimate_" class="">?</span><div class="price_box"> <label for="add_estimate__estimate__time_amount" class="top">Time:</label>
<span id="add_estimate__estimate__time_amount">?</span>
<label for="add_estimate__estimate__distance_amount" >Distance:</label>
<span id="add_estimate__estimate__distance_amount" >?</span>
<label for="add_estimate__estimate__fee_amount">Fees:</label>
<span id="add_estimate__estimate__fee_amount">?</span>
<label for="add_estimate__estimate__tax_amount" id="add_estimate__estimate__tax_summary_label"  class="bottom">Total&nbsp;Tax</label>
<span id="add_estimate__estimate__tax_amount">?</span></div></div><div class="cost"><div id="add_available_credit__available_credit__div"><label for="add_available_credit__available_credit_">AVAILABLE CREDIT:</label><span id="add_available_credit__available_credit_" class=""></span></div><div id="add_credit__balance__div"><label for="add_credit__balance_">APPLIED CREDIT:</label><span id="add_credit__balance_" class=""></span></div><div id="add_amount_due__amount_due__div"><label for="add_amount_due__amount_due_">AMOUNT DUE:</label><span id="add_amount_due__amount_due_" class="amount_due"></span><div class="instruction">NOTE: By clicking the "reserve it" button, your card will be billed the "amount due" shown above. <p>Any excess will be available for future reservations.  Distance is estimated at 7 miles per reserved hour.</p></div></div></div><div id="add_timeline___track" class="timeline slider"><div class="slider reservation good_reservation" id="reservation_bar"></div><div class="slider handle start" id="reservation_bar_start_handle"></div><div class="slider handle end" id="reservation_bar_end_handle"></div><ul class="segments" id="reservation_bar_track"><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="bad pad_end"></li><li class="bad"></li><li class="bad"></li><li class="bad pad_end"></li></ul></li><li ><ul ><li class="free pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li ><ul ><li class="good pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li ><ul ><li class="good pad_end"></li><li class="good"></li><li class="good"></li><li class="good pad_end"></li></ul></li><li ><ul ><li class="good pad_end"></li><li class="free"></li><li class="free"></li><li class="free pad_end"></li></ul></li></ul><img src="/skin/img/day_gauge.gif" /></div><div id="add_timeline__error" class="slider error_display"></div><div id='optional_rate_plan_adjustment' style='text-align:left;'><font class='text'></font></div><button id="lb_cancel_button" class="cancel"></button><button id="lb_reserve_button" class="reserve"></button></div></form><br style="clear: both;" /></div></div><script language="javascript" type="text/javascript">MV.globals.reserve.lightbox = new MV.controls.reserve.lightbox({"range_params":{"start_control":{"date_id":"add_start_stamp__start_date_","time_id":"add_start_stamp__start_time_"},"end_control":{"date_id":"add_end_stamp__end_date_","time_id":"add_end_stamp__end_time_"}},"estimate_params":{"price_id":"add_price__price_","available_balance_id":"add_balance__balance_","amount_due_id":"add_amount_due__amount_due_","credit_id":"add_credit__balance_","credit_box_id":"add_credit__balance__div","available_credit_box_id":"add_available_credit__available_credit__div","available_credit_id":"add_available_credit__available_credit_","cost_params":{"id":"add_estimate__estimate_","time_id":"add_estimate__estimate__time_amount","distance_id":"add_estimate__estimate__distance_amount","fees_id":"add_estimate__estimate__fee_amount","tax_id":"add_estimate__estimate__tax_amount","tax_pks":[],"labels":{"please_wait":"Please wait...","hourly":"Hourly","daily":"Daily"}},"hide_ab_shortfall":false},"accept_button_id":"lb_reserve_button","cancel_button_id":"lb_cancel_button","instruction_id":"lightbox_instruction","form_id":"add","attach_close_event":true,"attach_confirm_event":true,"use_dynamic_timeline":true,"initial_update":true,"preserve_instruction":true,"is_lightbox":true,"disabled_class":"reserve_disabled","slider_params":{"action":"add","stack_pk":"91800598","reservation_pk":0,"start_stamp":"1283753700","start_stamp_min":1283752800,"start_stamp_max":1293771600,"end_stamp":"1283764500","end_stamp_min":1283752800,"end_stamp_max":1293771600,"start_date_control":"add_start_stamp__start_date_","start_time_control":"add_start_stamp__start_time_","end_date_control":"add_end_stamp__end_date_","end_time_control":"add_end_stamp__end_time_","lower":1283680800,"upper":1283767200,"increment":900,"date_calibration":"09\/05\/10","control_ids":{"track_id":"reservation_bar_track","start_handle_id":"reservation_bar_start_handle","end_handle_id":"reservation_bar_end_handle","res_marker_id":"reservation_bar","error_id":"add_timeline__error"},"no_slider":false,"error_label":"Please adjust your times to an available period. Use the form above or click-and-drag your times."}});</script></body></html>'''
        from util.BeautifulSoup import BeautifulSoup
        html_data = BeautifulSoup(html_body)
        
        # When...
        vehicle = self.source.create_vehicle_from_pcs_information_doc(html_data)
        
        # Then...
        self.assertEqual(vehicle.id, '91800598')
        self.assertEqual(vehicle.model.name, 'Tacoma Pickup')
    
    def testShouldReturnVehiclePriceEstimateBodyFromThePcsConnection(self):
        class StubResponse (object):
            def read(self):
                return 'my body'
            def getheaders(self):
                return 'my head'
        
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.url = url
                self.method = method
                self.data = data
                self.headers = headers
                return StubResponse()
        StubConnection = Stub(PcsConnection)(StubConnection)
        conn = StubConnection()
        
        sessionid = 'ses1234'
        vehicleid = 'veh1234'
        start_time = datetime.datetime.fromtimestamp(100, Eastern)
        end_time = datetime.datetime.fromtimestamp(1000, Eastern)
        
        body, head = self.source.vehicle_price_estimate_from_pcs(conn, sessionid, vehicleid, start_time, end_time)
        
        self.assertEqual(conn.url, 'http://res.pcs.org/price.php?mv_action=add&stack_pk=veh1234&start_stamp=100&end_stamp=1000')
        self.assertEqual(conn.method, 'GET')
        self.assertEqual(conn.data, {})
        self.assertEqual(conn.headers, {'Cookie':'sid=ses1234'})
        self.assertEqual(body, 'my body')
    
    def testShouldCreatePriceEstimateFromJsonObject(self):
        test_body = r'''{"is_valid":true,"available_balance":[3.2,"$3.20"],"available_credit":[1.6,"$1.60"],"applied_credit":[1.7,"$1.70"],"show_credit_box":"no","show_available_credit":"no","start_date":"09\/08\/10","start_time":52200,"end_date":"09\/09\/10","end_time":58500,"reservation_pk":["6285517_25885382_1283970600_1284063300","$6285517.00"],"time_amount":[58.54,"$58.54"],"distance_amount":[24,"$24.00"],"fee_amount":[0,"$0.00"],"total_amount":[94.79,"$94.79"],"distance":[96,"96 mile(s)"],"hourly_rate":["5.450","$5.45"],"daily_rate":["49.000","$49.00"],"tax_amount":[12.25,"$12.25"],"tax_items":[{"pk":1,"amount":[6.6,"$6.60"]},{"pk":3,"amount":[1.65,"$1.65"]},{"pk":2,"amount":[4,"$4.00"]}],"optional_adjustment_pks":[],"descr":["descr","&nbsp;"],"rate_notice":"","estimate":[94.79,"$94.79"],"show_available_credit_box":"no","amount_due":[94.79,"<span class=\"owing\">$94.79<\/span>"],"driver_pk":"6285517","pk":"0","stack_pk":"25885382","optional_adjustment_html":"<font class='text'><\/font>"}'''
        
        try:
            import json
        except ImportError:
            from django.utils import simplejson as json
        
        json_data = json.loads(test_body)
        
        price = self.source.create_price_from_pcs_price_estimate_doc(json_data)
        
        self.assertEqual(price.available_balance, 3.20)
        self.assertEqual(price.available_credit, 1.60)
        self.assertEqual(price.applied_credit, 1.70)
        self.assertEqual(price.time_amount, 58.54)
        self.assertEqual(price.distance_amount, 24.00)
        self.assertEqual(price.fee_amount, 0.00)
        self.assertEqual(price.total_amount, 94.79)
        self.assertEqual(price.distance, 96)
        self.assertEqual(price.tax_amount, 12.25)
        self.assertEqual(price.amount_due, 94.79)
    
    def testShouldReturnPriceEstimateAsCreatedFromJsonData(self):
        @patch(self.source)
        def create_host_connection(self):
            return 'my connection'
        
        @patch(self.source)
        def vehicle_price_estimate_from_pcs(self, conn, sessionid, vehicleid, start_time, end_time):
            self.gpe_conn = conn
            self.gpe_sessionid = sessionid
            self.gpe_vehicleid = vehicleid
            self.gpe_start_time = start_time
            self.gpe_end_time = end_time
            return ('my body', 'my head')
        
        @patch(self.source)
        def get_json_data(self, response_body):
            self.gjd_price_body = response_body
            return 'my json data'
        
        @patch(self.source)
        def create_price_from_pcs_price_estimate_doc(self, json_price_obj):
            self.cp_price_obj = json_price_obj
            return 'my price'
        
        sessionid = 'ses1234'
        vehicleid = 'veh1234'
        start_time = 100
        end_time = 1000
        
        price = self.source.get_vehicle_price_estimate(sessionid, vehicleid, start_time, end_time)
        
        self.assertEqual(self.source.gpe_conn, 'my connection')
        self.assertEqual(self.source.gpe_sessionid, 'ses1234')
        self.assertEqual(self.source.gpe_vehicleid, 'veh1234')
        self.assertEqual(self.source.gpe_start_time, 100)
        self.assertEqual(self.source.gpe_end_time, 1000)
        self.assertEqual(self.source.gjd_price_body, 'my body')
        self.assertEqual(self.source.cp_price_obj, 'my json data')
        self.assertEqual(price, 'my price')
    
    
class LocationAvailabilityHtmlHandlerTest (unittest.TestCase):
    def testShouldBeInitializedWithHtmlViewsAndScreenscrapeSources(self):
        handler = LocationAvailabilityHtmlHandler()
        
        from pcs.source.screenscrape.session import SessionScreenscrapeSource
        from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
        from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
        from pcs.view.html.availability import AvailabilityHtmlView
        
        self.assertEqual(handler.vehicle_view.__class__.__name__,
                         AvailabilityHtmlView.__name__)
        self.assertEqual(handler.vehicle_source.__class__.__name__,
                         AvailabilityScreenscrapeSource.__name__)
        self.assertEqual(handler.location_source.__class__.__name__,
                         LocationsScreenscrapeSource.__name__)
        self.assertEqual(handler.session_source.__class__.__name__,
                         SessionScreenscrapeSource.__name__)
    
    
class LocationAvailabilityJsonHandlerTest (unittest.TestCase):
    def testShouldBeInitializedWithJsonViewsAndScreenscrapeSources(self):
        handler = LocationAvailabilityJsonHandler()
        
        from pcs.source.screenscrape.session import SessionScreenscrapeSource
        from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
        from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
        from pcs.view.json.availability import AvailabilityJsonView
        
        self.assertEqual(handler.vehicle_view.__class__.__name__,
                         AvailabilityJsonView.__name__)
        self.assertEqual(handler.vehicle_source.__class__.__name__,
                         AvailabilityScreenscrapeSource.__name__)
        self.assertEqual(handler.location_source.__class__.__name__,
                         LocationsScreenscrapeSource.__name__)
        self.assertEqual(handler.session_source.__class__.__name__,
                         SessionScreenscrapeSource.__name__)


class AvailabilityHtmlViewTest (unittest.TestCase):
    def testShouldPassVariablesToTheTemplateCorrectly(self):
        self.path = None
        self.values = None
        
        def stub_render_method(stub_path, stub_values):
            self.path = stub_path
            self.values = stub_values
            return 'the rendering'
        
        session = 'my session'
        location = 'my location'
        start_time = datetime.datetime(2010,11,1,tzinfo=Eastern)
        end_time = datetime.datetime(2011,1,1,tzinfo=Eastern)
        vehicle_availabilities = ['v1','v2']
        view = AvailabilityHtmlView(stub_render_method)
        
        rendering = view.render_location_availability(session, location, start_time, end_time, vehicle_availabilities)
        
        self.assertEqual(self.values, {'session':'my session', 'location':'my location', 'start_time':datetime.datetime(2010,11,1,tzinfo=Eastern), 'end_time':datetime.datetime(2011,1,1,tzinfo=Eastern), 'start_stamp': 1288584000, 'end_stamp': 1293858000, 'vehicle_availabilities':['v1','v2']})
        self.assertEqual(rendering, 'the rendering')


class AvailabilityJsonViewTest (unittest.TestCase):
    def testShouldPassVariablesToTheTemplateCorrectly(self):
        self.path = None
        self.values = None
        
        def stub_render_method(stub_path, stub_values):
            self.path = stub_path
            self.values = stub_values
            return 'the rendering'
        
        session = 'my session'
        location = 'my location'
        start_time = datetime.datetime(2010,11,1,tzinfo=Eastern)
        end_time = datetime.datetime(2011,1,1,tzinfo=Eastern)
        vehicle_availabilities = ['v1','v2']
        view = AvailabilityJsonView(stub_render_method)
        
        rendering = view.render_location_availability(session, location, start_time, end_time, vehicle_availabilities)
        
        self.assertEqual(self.values, {'session':'my session', 'location':'my location', 'start_time':datetime.datetime(2010,11,1,tzinfo=Eastern), 'end_time':datetime.datetime(2011,1,1,tzinfo=Eastern), 'start_stamp': 1288584000, 'end_stamp': 1293858000, 'vehicle_availabilities':['v1','v2']})
        self.assertEqual(rendering, 'the rendering')
    
    def testShouldRenderLocationAvailabilityCorrectly(self):
    		class StubData (object):
    				pass
    		
    		session = StubData()
    		location = StubData()
    		location.id = 'location id'
    		location.name = 'location name'
    		start_time = datetime.datetime(2010,11,1,2,30,tzinfo=Eastern)
    		end_time = datetime.datetime(2011,1,1,5,15,tzinfo=Eastern)
    		
    		vav1 = StubData()
    		vav1.earliest = datetime.datetime(2010,11,1,3,15,tzinfo=Eastern)
    		vav1.vehicle = StubData()
    		vav1.vehicle.pod = StubData()
    		vav1.vehicle.pod.id = 'p1'
    		vav1.vehicle.pod.name = 'pod 1'
    		vav1.vehicle.model = StubData()
    		vav1.vehicle.model.name = 'model 1'
    		
    		vav2 = StubData()
    		vav2.vehicle = StubData()
    		vav2.vehicle.pod = StubData()
    		vav2.vehicle.pod.id = 'p1'
    		vav2.vehicle.pod.name = 'pod 1'
    		vav2.vehicle.model = StubData()
    		vav2.vehicle.model.name = 'model 2'
    		
    		vav3 = StubData()
    		vav3.latest = datetime.datetime(2010,11,1,4,45,tzinfo=Eastern)
    		vav3.vehicle = StubData()
    		vav3.vehicle.pod = StubData()
    		vav3.vehicle.pod.id = 'p2'
    		vav3.vehicle.pod.name = 'pod 2'
    		vav3.vehicle.model = StubData()
    		vav3.vehicle.model.name = 'model 1'
    		
    		vehicle_availabilities = [vav1, vav2, vav3]
    		view = AvailabilityJsonView()
    		rendering = view.render_location_availability(session, location, start_time, end_time, vehicle_availabilities)
    		
    		self.assertEqual(
"""{"location_availability" : {
	"location" : {
		"id" : "location id",
		"name" : "location name"
	} ,
	"start_time" : "2010-11-01T02:30",
	"end_time" : "2011-01-01T05:15",
	"vehicle_availabilities" : [

		{
			"vehicle" : {
				"pod" : {
					"id" : "p1",
					"name" : "pod 1"} ,
				"model" : {
					"id" : "",
					"name" : "model 1"}} ,
			"earliest" : "2010-11-01T03:15",
			"latest" : ""
		} ,

		{
			"vehicle" : {
				"pod" : {
					"id" : "p1",
					"name" : "pod 1"} ,
				"model" : {
					"id" : "",
					"name" : "model 2"}} ,
			"earliest" : "",
			"latest" : ""
		} ,

		{
			"vehicle" : {
				"pod" : {
					"id" : "p2",
					"name" : "pod 2"} ,
				"model" : {
					"id" : "",
					"name" : "model 1"}} ,
			"earliest" : "",
			"latest" : "2010-11-01T04:45"
		}

	]
}}""",
    		rendering)
