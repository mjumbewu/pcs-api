import unittest

class LocationAvailabilityJsonHandlerBlackBoxTest (unittest.TestCase):
    def testGivenCoordinatesShouldRespondWithCorrectVehicles(self):
        # This is an integration test against the server, so we're going to 
        # have to log in first.
        import private_info as priv
        from pcs.wsgi_handlers.session import SessionJsonHandler
        
        class StubRequest (dict):
            pass
        
        class StubHeaders (dict):
            def add_header(self, key, val):
                self[key]=val
        
        import StringIO
        class StubResponse (object):
            def __init__(self):
                self.out = StringIO.StringIO()
                self.headers = StubHeaders()
            def set_status(self, status):
                self.status = status
        
        session_handler = SessionJsonHandler()
        session_handler.request = StubRequest()
        session_handler.response = StubResponse()
        
        session_handler.request['user'] = priv.USERID
        session_handler.request['password'] = priv.PASSWORD
        
        session_handler.post()
        
        # Now use the cookie from the session for the location availability.
        from pcs.wsgi_handlers.availability import LocationAvailabilityJsonHandler
        handler = LocationAvailabilityJsonHandler()
        handler.request = StubRequest()
        handler.response = StubResponse()
        
        handler.request.cookies = {
            'session':session_handler.response.headers['Set-Cookie'][8:-8]}
        handler.get('39.954162,-75.171182')
        
        try:
            import json
        except ImportError:
            from django.utils import simplejson as json
        
        # The first pod should be 18th & JFK
        result = json.loads(handler.response.out.getvalue())
        self.assertEqual(result['location_availability']['vehicle_availabilities'][0]['vehicle']['pod']['name'], '18th & JFK')



