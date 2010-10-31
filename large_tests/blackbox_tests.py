import unittest

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from util.testing import patch
from util.testing import Stub

########################################
# Some stubs for requests and responses.
#
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
#
########################################

class RestInterfaceBlackBoxTest (unittest.TestCase):
    def sign_in_and_get_session_cookie(self):
        # These are integration tests against the server, so we're going to 
        # have to log in first.
        import private_info as priv
        from pcs.wsgi_handlers.session import SessionJsonHandler
        
        session_handler = SessionJsonHandler()
        session_handler.request = StubRequest()
        session_handler.response = StubResponse()
        
        session_handler.request['user'] = priv.USERID
        session_handler.request['password'] = priv.PASSWORD
        
        session_handler.post()
        session_cookie = session_handler.response.headers['Set-Cookie'][8:-8]
        return session_cookie
    
    def initialize_handler_for_session(self, handler, session_cookie):
        # Give the handler a request object already set up with the session
        # cookie, and response object ready for content.
        handler.request = StubRequest()
        handler.response = StubResponse()
        
        handler.request.cookies = {'session':session_cookie}
    
    def testGivenCoordinatesShouldRespondWithCorrectVehiclesNearLocation(self):
        session_cookie = self.sign_in_and_get_session_cookie()
        
        # Now use the cookie from the session for the location availability.
        from pcs.wsgi_handlers.availability import LocationAvailabilityJsonHandler
        handler = LocationAvailabilityJsonHandler()
        self.initialize_handler_for_session(handler, session_cookie)
        
        handler.get('39.954162,-75.171182')
        
        response_body = handler.response.out.getvalue()
        
        # The first pod should be 18th & JFK
        result = json.loads(response_body)
        self.assertEqual(result['location_availability']['vehicle_availabilities'][0]['vehicle']['pod']['name'], '18th & JFK')
    
    def testGivenValidTimeShouldRespondWithReservationConfirmation(self):
        session_cookie = self.sign_in_and_get_session_cookie()
        
        from pcs.wsgi_handlers.reservations import ReservationsJsonHandler
        handler = ReservationsJsonHandler()
        self.initialize_handler_for_session(handler, session_cookie)
        
        vehicleid = 96692246 # A Prius at 47th & Baltimore
        start_time, end_time = handler.get_single_iso_datetime_range()
        
        from datetime import timedelta as td
        from util.TimeZone import current_time, to_isostring
        now = current_time()
        three_days = td(days=3)
        later = now + three_days
        
        start_time = later.replace(hour=3, minute=15)
        end_time = later.replace(hour=3, minute=30)
        
        handler.request['vehicle'] = str(vehicleid)
        handler.request['start_time'] = to_isostring(start_time)
        handler.request['end_time'] = to_isostring(end_time)
        handler.request['memo'] = 'blackbox reservation test'
        
        handler.post()
        
        response_body = handler.response.out.getvalue()
        
        # I should get a confirmation
        response = json.loads(response_body)
        error = response.get('error', None)
        self.assert_(error is None, (error is None) or
                     error['msg'] + '\n' + error['detail'] + '\n' + error['msg'])
        
        confirmation = response.get('confirmation', None)
        self.assert_(confirmation is not None)
        self.assertEqual(confirmation['reservation']['vehicle']['id'], '96692246')
        

