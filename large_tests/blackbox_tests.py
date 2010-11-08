import unittest
import datetime

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from util.testing import patch
from util.testing import Stub
from util.TimeZone import current_time, to_isostring

########################################
# Some stubs for requests and responses.
#
class StubRequest (dict):
    def __init__(self):
        self.headers = {}
        self.query_string = ''
        self.body = ''
    
    def arguments(self):
        return []

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
    session_cookie = None
    
    def sign_in_and_get_session_cookie(self):
        # These are integration tests against the server, so we're going to 
        # have to log in first (but we might as well cache it).
        if self.session_cookie is None:
            
            import private_info as priv
            from pcs.wsgi_handlers.session import SessionJsonHandler
            
            session_handler = SessionJsonHandler()
            session_handler.request = StubRequest()
            session_handler.response = StubResponse()
            
            session_handler.request['user'] = priv.USERID
            session_handler.request['password'] = priv.PASSWORD
            
            session_handler.post()
            
            response_body = session_handler.response.out.getvalue()
            response = json.loads(response_body)
            self.check_for_error(response)
            
            # Trim off 'session_id=' and the trailing ';'
            session_cookie = session_handler.response.headers['Set-Cookie'][11:-1]
            
            self.session_cookie = session_cookie
        
        return self.session_cookie
    
    def initialize_handler_for_session(self, handler, session_cookie):
        # Give the handler a request object already set up with the session
        # cookie, and response object ready for content.
        handler.request = StubRequest()
        handler.response = StubResponse()
        
        handler.request.cookies = {'session_id':session_cookie}
    
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
    
    def check_for_error(self, response):
        error = response.get('error', None)
        self.assert_(error is None, (error is None) or
                     error['msg'] + '\n' + error['detail'] + '\n' + error['msg'])
    
    def testMakeChangeAndCancelAReservation(self):
        
        # This is a long test that will exercise the whole process of making,
        # checking, editing, and canceling a reservation.  It really is a long
        # test (on the order of 30 seconds), so make sure you're all unit-tested
        # up before running it; don't expect to make it a part of your regular
        # tests.
        
        session_cookie = self.sign_in_and_get_session_cookie()
        
        #######################################################################
        # First, make a reservation
        from pcs.wsgi_handlers.reservations import ReservationsJsonHandler
        handler = ReservationsJsonHandler()
        self.initialize_handler_for_session(handler, session_cookie)
        
        vehicleid = '96692246' # A Prius at 47th & Baltimore
        
        now = current_time()
        three_days = datetime.timedelta(days=3)
        later = now + three_days
        
        start_time = later.replace(hour=3, minute=00)
        end_time = later.replace(hour=3, minute=15)
        
        handler.request['vehicle'] = vehicleid
        handler.request['start_time'] = to_isostring(start_time)
        handler.request['end_time'] = to_isostring(end_time)
        handler.request['memo'] = 'reservation create test'
        
        handler.post()
        
        response_body = handler.response.out.getvalue()
        
        # I should get a confirmation
        response = json.loads(response_body)
        self.check_for_error(response)
        
        confirmation = response.get('confirmation', None)
        self.assert_(confirmation is not None)
        self.assertEqual(confirmation['reservation']['vehicle']['id'], vehicleid)
        
        liveid = confirmation['reservation'].get('liveid', None)
        self.assert_(liveid is not None, response_body)
        
        #######################################################################
        # Now, use the liveid from above to change the reservation
        from pcs.wsgi_handlers.reservations import ReservationJsonHandler
        handler = ReservationJsonHandler()
        self.initialize_handler_for_session(handler, session_cookie)
        
        start_time = later.replace(hour=3, minute=45)
        end_time = later.replace(hour=4, minute=00)
        
        handler.request['vehicle'] = vehicleid
        handler.request['start_time'] = to_isostring(start_time)
        handler.request['end_time'] = to_isostring(end_time)
        handler.request['memo'] = 'reservation modify test'
        
        handler.put(liveid)
        
        response_body = handler.response.out.getvalue()
        
        # I should get a confirmation
        response = json.loads(response_body)
        self.check_for_error(response)
        
        confirmation = response.get('confirmation', None)
        self.assert_(confirmation is not None)
        self.assertEqual(confirmation['reservation']['liveid'], liveid)
        self.assertEqual(confirmation['reservation']['vehicle']['id'], vehicleid)
        
        #######################################################################
        # Get the reservation information, using the same liveid
        from pcs.wsgi_handlers.reservations import ReservationJsonHandler
        handler = ReservationJsonHandler()
        self.initialize_handler_for_session(handler, session_cookie)
        
        handler.get(liveid)
        
        response_body = handler.response.out.getvalue()
        
        # I should get a reservation consistent with the one I just modified
        response = json.loads(response_body)
        self.check_for_error(response)
        
        reservation = response.get('reservation', None)
        self.assert_(reservation is not None)
        self.assertEqual(reservation['liveid'], liveid)
        self.assertEqual(reservation['vehicle']['id'], vehicleid)
        self.assertEqual(reservation['start_time'], to_isostring(start_time)[:16])
        self.assertEqual(reservation['end_time'], to_isostring(end_time)[:16])
        self.assertEqual(reservation['vehicle']['model']['name'], 'Prius Liftback')
        self.assertEqual(reservation['vehicle']['pod']['name'], '47th & Baltimore')
        self.assertEqual(reservation['vehicle']['pod']['id'], '30005')
        self.assertEqual(reservation['memo'], 'reservation modify test')
        
        #######################################################################
        # Now cancel the reservation
        handler = ReservationJsonHandler()
        self.initialize_handler_for_session(handler, session_cookie)
        
        handler.request['vehicle'] = vehicleid
        handler.request['start_time'] = to_isostring(start_time)
        handler.request['end_time'] = to_isostring(end_time)
        
        handler.delete(liveid)
        
        response_body = handler.response.out.getvalue()
        
        # I should get a confirmation
        response = json.loads(response_body)
        self.check_for_error(response)
        
        confirmation = response.get('confirmation', None)
        self.assert_(confirmation is not None)
        self.assertEqual(confirmation['reservation']['liveid'], liveid)
        self.assertEqual(confirmation['reservation']['vehicle']['id'], vehicleid)

