import unittest
import datetime
import new

from pcs.data.session import Session
from pcs.input.wsgi.locations import LocationsHandler
from pcs.source import _LocationsSourceInterface
from pcs.source import _SessionSourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from pcs.view import _LocationsViewInterface
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
            def get_locations(self, session, locations):
                if session:
                    return "Success"
                else:
                    return "Failure"
        
        # The system under test
        self.session_source = StubSessionSource()
        self.locations_source = StubLocationsSource()
        self.locations_view = StubLocationsView()
        
        self.handler = LocationsHandler(session_source=self.session_source, 
            locations_source=self.locations_source,
            locations_view=self.locations_view)
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
    
    def testShouldRespondSuccessfullyWhenGivenAValidSession(self):
        # Given...
        self.handler.request.cookies = {
            'sid': '123abc',
            'suser': 'userid123'
        }
        
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            session = Session('123abc', 'me', 'My Account')
            return session
        
        # When...
        self.handler.get()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assertEqual(response_body, 'Success')
    
    def testShouldGenerateAFailureWhenGivenAnInvalidSession(self):
        # Given...
        self.handler.request.cookies = {
            'sid': '123abc',
            'suser': 'userid123'
        }
        
        @patch(self.session_source)
        def get_existing_session(self, userid, sessionid):
            return None
        
        self.handler._saved_exception = None
        @patch(self.handler)
        def generate_error(self, exception):
            self._saved_exception = exception
            return 'Failure'
        
        # When...
        self.handler.get()
        
        # Then...
        self.assert_(self.handler._saved_exception is not None)
        self.assertEqual(type(self.handler._saved_exception).__name__, 'AttributeError')
    

from pcs.source.screenscrape.locations import LocationsScreenscrapeSource
class LocationsScreenscrapeSourceTest (unittest.TestCase):
    def testShouldConstructExpectedLocationProfilesFromPcsConnectionContent(self):
        # Given...
        class StubConnection (object):
            def request(self, method, path, data, headers):
                pass
            def getresponse(self):
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
        class StubConnection (object):
            def request(self, method, path, data, headers):
                pass
            def getresponse(self):
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
    
    def testShouldReturnFailureDocumentIfPrefsRequestGoesWrong(self):
        # Given...
        class MyCustomException (Exception):
            pass
        
        class StubConnection (object):
            def request(self, method, path, data, headers):
                pass
            def getresponse(self):
                raise MyCustomException()
        
        conn = StubConnection()
        source = LocationsScreenscrapeSource()
        
        # When...
        try:
            response_body, headers = \
                source.get_preferences_response(conn=conn, sessionid='abc')
        
        # Then...
        except MyCustomException:
            self.fail('Exception should have been caught and handled')
        
        self.assertEqual(response_body, LocationsScreenscrapeSource.SIMPLE_FAILURE_DOCUMENT)
    
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
        class StubConnection (object):
            def request(self, method, path, data, headers):
                pass
            def getresponse(self):
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

