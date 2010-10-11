import unittest
import datetime
import new

from pcs.data.session import Session
from pcs.input.wsgi.locations import LocationsHandler
from pcs.input.wsgi.locations import LocationsJsonHandler
from pcs.source import _LocationsSourceInterface
from pcs.source import _SessionSourceInterface
from pcs.source import SessionExpiredError
from pcs.source.screenscrape import ScreenscrapeParseError
from pcs.source.screenscrape.pcsconnection import PcsConnection
from pcs.view import _ErrorViewInterface
from pcs.view import _LocationsViewInterface
from pcs.view.json.locations import LocationsJsonView
from util.testing import patch
from util.testing import Stub

class LocationHandlerTest (unittest.TestCase):
    
    def setUp(self):
        # A fake request class
        class StubRequest (dict):
            cookies = {}
        
        # A fake response class
        import StringIO
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
        
        # A source for session information
        @Stub(_SessionSourceInterface)
        class StubSessionSource (object):
            pass
        
        # A source for vehicle availability information
        @Stub(_LocationsSourceInterface)
        class StubLocationsSource (object):
            def get_location_profiles(self, sessionid):
                pass
        
        # A generator for a representation (view) of the availability information
        @Stub(_LocationsViewInterface)
        class StubLocationsView (object):
            def render_locations(self, session, locations):
                if session:
                    return "Success"
                else:
                    return "Failure"
        
        @Stub(_ErrorViewInterface)
        class StubErrorView (object):
            pass
        
        # The system under test
        self.session_source = StubSessionSource()
        self.locations_source = StubLocationsSource()
        self.locations_view = StubLocationsView()
        self.error_view = StubErrorView()
        
        self.handler = LocationsHandler(session_source=self.session_source, 
            locations_source=self.locations_source,
            locations_view=self.locations_view,
            error_view=self.error_view)
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
    
    def testShouldRespondSuccessfullyWhenGivenAValidSession(self):
        # Given...
        @patch(self.handler)
        def get_user_id(self):
            self.userid_called = True
            return 'user1234'
        
        @patch(self.handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(self.handler)
        def get_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
        
        @patch(self.locations_source)
        def get_location_profiles(self, sessionid):
            self.sessionid = sessionid
            return 'my locations'
        
        @patch(self.locations_view)
        def render_locations(self, session, locations):
            self.session = session
            self.locations = locations
            return 'location profiles body'
        
        @patch(self.error_view)
        def render_error(self, error_code, error_msg):
            pass
        
        # When...
        self.handler.get()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assert_(self.handler.userid_called)
        self.assert_(self.handler.sessionid_called)
        self.assertEqual(self.handler.userid, 'user1234')
        self.assertEqual(self.handler.sessionid, 'ses1234')
        self.assertEqual(self.locations_source.sessionid, 'ses1234')
        self.assertEqual(self.locations_view.locations, 'my locations')
        self.assertEqual(self.locations_view.session, 'my session')
        self.assertEqual(response_body, 'location profiles body')
    
    def testShouldGenerateAFailureWhenGivenAnInvalidSession(self):
        # Given...
        @patch(self.handler)
        def get_user_id(self):
            self.userid_called = True
            return 'user1234'
        
        @patch(self.handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(self.handler)
        def get_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            raise SessionExpiredError()
        
        @patch(self.error_view)
        def render_error(self, error_code, error_msg):
            return error_msg
        
        # When...
        self.handler.get()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assert_(self.handler.userid_called)
        self.assert_(self.handler.sessionid_called)
        self.assertEqual(self.handler.userid, 'user1234')
        self.assertEqual(self.handler.sessionid, 'ses1234')
        self.assert_(response_body.startswith('SessionExpiredError'), 'Should start with SessionExpiredError: %r' % response_body)
    

from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
class LocationsScreenscrapeSourceTest (unittest.TestCase):
    def testShouldConstructExpectedLocationProfilesFromPcsConnectionContent(self):
        # Given...
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                import StringIO
                response = StringIO.StringIO(r'''<table><thead><tr id="dpref_driver_pk__preferences_pk__driver_locations_pk__header"><th>Default</th><th>Name</th><th>Description</th><th></th></tr></thead><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__noprofiles" style="display: none; "><tr><td colspan="4">You have no saved locations.</td></tr></tbody><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__profiles"><tr class=""><td><input type="radio" class="profile_default" value="18065565" checked="checked"></td><td class="profile_name">My House</td><td class="profile_descr"></td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class="zebra"><td><input type="radio" class="profile_default" value="25782103"></td><td class="profile_name">My Job</td><td class="profile_descr">Walnut St &amp; S 33rd St, Philadelphia, PA 19104, USA</td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class=""><td><input type="radio" class="profile_default" value="17966898"></td><td class="profile_name">Sprucemont</td><td class="profile_descr"></td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class="zebra"><td><input type="radio" class="profile_default" value="25618502"></td><td class="profile_name">UPenn Library</td><td class="profile_descr">Walnut St &amp; S 36th St, Philadelphia, PA 19104, USA</td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr></tbody><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__favourites"><tr class=""><td><input type="radio" class="profile_default" value="0"></td><td colspan="2">Favorites</td><td></td></tr><tr class="zebra"><td><input type="hidden" value="2041034"></td><td colspan="2">&nbsp;&nbsp;47th &amp; Baltimore - Scion xB</td><td><a href="javascript:void(0);" class="delete_favourite">Delete</a></td></tr><tr class=""><td><input type="hidden" value="4756298"></td><td colspan="2">&nbsp;&nbsp;47th &amp; Baltimore - Sienna Minivan</td><td><a href="javascript:void(0);" class="delete_favourite">Delete</a></td></tr></tbody></table>''')
                response.getheaders = lambda: {'h1':1}
                return response
        
        source = LocationsScreenscrapeSource()
        @patch(source)
        def create_connection(self):
            return StubConnection()
        
        # When...
        locations = source.get_location_profiles(sessionid='123abc')
        
        # Then...
        self.assertEqual(locations[0].name, 'My House')
        self.assertEqual(len(locations), 4)
        self.assertEqual(locations[3].name, 'UPenn Library')
    
    def testPreferencesResponseShouldBeAsExpectedFromConnection(self):
        # Given...
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                import StringIO
                response = StringIO.StringIO('MyBody')
                response.getheaders = lambda: {'h1':1}
                
                return response
        
        conn = StubConnection()
        source = LocationsScreenscrapeSource()
        
        # When...
        response_body, response_headers = \
            source.get_preferences_response(conn=conn, sessionid='123abc')
        
        # Then...
        self.assertEqual(response_body, 'MyBody')
        self.assertEqual(response_headers, {'h1':1})
    
    def testShouldParseLocationsFromResponseBody(self):
        # Given...
        prefs_body = r'''<html><body><table><thead><tr id="dpref_driver_pk__preferences_pk__driver_locations_pk__header"><th>Default</th><th>Name</th><th>Description</th><th></th></tr></thead><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__noprofiles" style="display: none; "><tr><td colspan="4">You have no saved locations.</td></tr></tbody><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__profiles"><tr class=""><td><input type="radio" class="profile_default" value="18065565" checked="checked"></td><td class="profile_name">My House</td><td class="profile_descr"></td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class="zebra"><td><input type="radio" class="profile_default" value="25782103"></td><td class="profile_name">My Job</td><td class="profile_descr">Walnut St &amp; S 33rd St, Philadelphia, PA 19104, USA</td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class=""><td><input type="radio" class="profile_default" value="17966898"></td><td class="profile_name">Sprucemont</td><td class="profile_descr"></td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class="zebra"><td><input type="radio" class="profile_default" value="25618502"></td><td class="profile_name">UPenn Library</td><td class="profile_descr">Walnut St &amp; S 36th St, Philadelphia, PA 19104, USA</td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr></tbody><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__favourites"><tr class=""><td><input type="radio" class="profile_default" value="0"></td><td colspan="2">Favorites</td><td></td></tr><tr class="zebra"><td><input type="hidden" value="2041034"></td><td colspan="2">&nbsp;&nbsp;47th &amp; Baltimore - Scion xB</td><td><a href="javascript:void(0);" class="delete_favourite">Delete</a></td></tr><tr class=""><td><input type="hidden" value="4756298"></td><td colspan="2">&nbsp;&nbsp;47th &amp; Baltimore - Sienna Minivan</td><td><a href="javascript:void(0);" class="delete_favourite">Delete</a></td></tr></tbody></table></body></html>'''
        source = LocationsScreenscrapeSource()
        
        # When...
        locations = source.parse_locations_from_preferences_body(prefs_body)
        
        # Then...
        self.assertEqual(len(locations), 4)
        
    def testShouldRaiseAnErrorWhenNoProfilesTbodyInResponse(self):
        # Given...
        prefs_body = r'Nobody'
        source = LocationsScreenscrapeSource()
        
        # When...
        try:
            locations = source.parse_locations_from_preferences_body(prefs_body)
        
        # Then...
        except ScreenscrapeParseError:
            return
        
        self.fail('Should have raised an exception')
    
    def testShouldReturnRequestedLocationProfile(self):
        # Given...
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                import StringIO
                response = StringIO.StringIO(r'''<table><thead><tr id="dpref_driver_pk__preferences_pk__driver_locations_pk__header"><th>Default</th><th>Name</th><th>Description</th><th></th></tr></thead><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__noprofiles" style="display: none; "><tr><td colspan="4">You have no saved locations.</td></tr></tbody><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__profiles"><tr class=""><td><input type="radio" class="profile_default" value="18065565" checked="checked"></td><td class="profile_name">My House</td><td class="profile_descr"></td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class="zebra"><td><input type="radio" class="profile_default" value="25782103"></td><td class="profile_name">My Job</td><td class="profile_descr">Walnut St &amp; S 33rd St, Philadelphia, PA 19104, USA</td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class=""><td><input type="radio" class="profile_default" value="17966898"></td><td class="profile_name">Sprucemont</td><td class="profile_descr"></td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr><tr class="zebra"><td><input type="radio" class="profile_default" value="25618502"></td><td class="profile_name">UPenn Library</td><td class="profile_descr">Walnut St &amp; S 36th St, Philadelphia, PA 19104, USA</td><td><a href="javascript:void(0);" class="profile_name">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" class="delete_profile">Delete</a></td></tr></tbody><tbody id="dpref_driver_pk__preferences_pk__driver_locations_pk__favourites"><tr class=""><td><input type="radio" class="profile_default" value="0"></td><td colspan="2">Favorites</td><td></td></tr><tr class="zebra"><td><input type="hidden" value="2041034"></td><td colspan="2">&nbsp;&nbsp;47th &amp; Baltimore - Scion xB</td><td><a href="javascript:void(0);" class="delete_favourite">Delete</a></td></tr><tr class=""><td><input type="hidden" value="4756298"></td><td colspan="2">&nbsp;&nbsp;47th &amp; Baltimore - Sienna Minivan</td><td><a href="javascript:void(0);" class="delete_favourite">Delete</a></td></tr></tbody></table>''')
                response.getheaders = lambda: {'h1':1}
                return response
        
        source = LocationsScreenscrapeSource()
        @patch(source)
        def create_connection(self):
            return StubConnection()
        
        # When...
        location = source.get_location_profile('123abc', '25782103')
        
        # Then...
        self.assertEqual(location.name, 'My Job')
        self.assertEqual(location.desc, 'Walnut St &amp; S 33rd St, Philadelphia, PA 19104, USA')
        self.assertEqual(location.id, '25782103')
    
    def testShouldReturnRequestedCustomLocation(self):
        # Given...
        source = LocationsScreenscrapeSource()
        
        # When...
        location = source.get_custom_location('Custom Location', (123,456))
        
        # Then...
        self.assertEqual(location.name, 'Custom Location')
        self.assertEqual(location.latitude, 123)
        self.assertEqual(location.longitude, 456)

class LocationsJsonHandlerTest (unittest.TestCase):
    def testShouldBeInitializedWithJsonViewsAndScreenscrapeSources(self):
        handler = LocationsJsonHandler()
        
        from pcs.source.screenscrape.session import SessionScreenscrapeSource
        from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
        from pcs.view.json.error import ErrorJsonView
        from pcs.view.json.locations import LocationsJsonView
        
        self.assertEqual(handler.error_view.__class__.__name__,
                         ErrorJsonView.__name__)
        self.assertEqual(handler.locations_view.__class__.__name__,
                         LocationsJsonView.__name__)
        self.assertEqual(handler.locations_source.__class__.__name__,
                         LocationsScreenscrapeSource.__name__)
        self.assertEqual(handler.session_source.__class__.__name__,
                         SessionScreenscrapeSource.__name__)

class LocationsJsonViewTest (unittest.TestCase):
    def testShouldRenderLocationAvailabilityCorrectly(self):
    		class StubData (object):
    				pass
    		
    		session = StubData()
    		
    		l1 = StubData()
    		l1.id = 'l1'
    		l1.name = 'location 1'
    		l1.is_default = False
    		
    		l2 = StubData()
    		l2.id = 'l2'
    		l2.name = 'location 2'
    		l2.is_default = True
    		
    		l3 = StubData()
    		l3.id = (123,456)
    		l3.name = 'location 3'
    		l3.is_default = False
    		
    		locations = [l1, l2, l3]
    		view = LocationsJsonView()
    		rendering = view.render_locations(session, locations)
    		
    		self.assertEqual(
"""{"locations" : [

	{
		"id" : "l1",
		"name" : "location 1",
		"is_default" : false
	} ,

	{
		"id" : "l2",
		"name" : "location 2",
		"is_default" : true
	} ,

	{
		"id" : "(123, 456)",
		"name" : "location 3",
		"is_default" : false
	}

]}
""",
    		rendering)
