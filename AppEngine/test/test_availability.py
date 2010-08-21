import unittest
import datetime
import new

from pcs.input.wsgi.availability import AvailabilityHandler
class AvailabilityHandlerTest (unittest.TestCase):
    
    def setUp(self):
        # A fake request class
        class StubRequest (object):
            def get(self, var):
                vals = {
                  'start_time':'100',
                  'end_time':'10000',
                }
                return vals[var]
        
        # A fake response class
        import StringIO
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
        
        # A source for session information (note: should be called SessionSource)
        class StubLoginSource (object):
            pass
        
        # A generator for a representation (view) of the availability information
        class StubAvailabilityView (object):
            def get_vehicle_availability(self, session, start_time, end_time, vehicles):
                if session:
                    return "Success"
                else:
                    return "Failure"
        
        # The system under test
        self.login_source = StubLoginSource()
        self.availability_view = StubAvailabilityView()
        
        self.handler = AvailabilityHandler(login_source=self.login_source, 
            availability_view=self.availability_view)
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
        
    def testShouldRespondWithFailureContentWhenSessionSourceCannotFindSessionWithGivenId(self):
        """With no valid session, the availability handler will give a failure document response."""
        
        # Given...
        # ...the session cookies are as follows:
        self.handler.request.cookies = {
          'sid':'5',
          'suser':'4600'
        }
        
        # ...and the session source does not recognize the cookies:
        def get_existing_session_patch(self, userid, sessionid):
            return None
        self.login_source.get_existing_session = \
            new.instancemethod(get_existing_session_patch, 
                self.login_source, self.login_source.__class__)
        
        # When...
        self.handler.get()
        
        # Then...
        response = self.handler.response.out.getvalue()
        self.assertEqual(response, "Failure")

    def testShouldRespondWithSuccessContentWhenSessionSourceRecognizesGivenSessionId(self):
        """With a valid session, the availability handler will give a success response."""
        
        # Given...
        # ...the session cookies are as follows:
        self.handler.request.cookies = {
          'sid':'5',
          'suser':'4600'
        }
        
        # ...and the session source recognizes the cookies:
        def get_existing_session_patch(self, userid, sessionid):
            class StubSession (object):
                id = 5
                user = '4600'
                name = "Jim Jacobsen"
            return StubSession()
        self.login_source.get_existing_session = \
            new.instancemethod(get_existing_session_patch, 
                self.login_source, self.login_source.__class__)
        
        # When...
        self.handler.get()
        
        # Then...
        response = self.handler.response.out.getvalue()
        self.assertEqual(response, "Success")
    
from pcs.view.html.availability import AvailabilityHtmlView
class AvailabilityHtmlViewTest (unittest.TestCase):
    def testShouldReturnHtmlContentReflectingVehicleAvailability(self):
        """The HTML view returned by get_vehicle_availability should reflect the data given."""
        
        # Given...
        class StubSession (object):
            pass
        
        class StubPod (object):
            pass
        
        class StubVehicle (object):
            pass
        
        session = StubSession()
        
        p1 = StubPod(); p1.id = 1; p1.name = "Pod 1"
        p2 = StubPod(); p2.id = 2; p2.name = "Pod 2"
        
        v1 = StubVehicle()
        v1.id = 3
        v1.pod = p1
        v1.availability = 1
        v1.make = 'Toyota'
        v1.model = 'Prius'
        
        v2 = StubVehicle()
        v2.id = 4
        v2.pod = p1
        v2.availability = 0.5
        v2.make = 'Toyota'
        v2.model = 'Prius'
        v2.available_at = datetime.datetime.fromtimestamp(4000)
        
        v3 = StubVehicle()
        v3.id = 5
        v3.pod = p1
        v3.availability = 1
        v3.make = 'Toyota'
        v3.model = 'Prius'
        
        v4 = StubVehicle()
        v4.id = 6
        v4.pod = p2
        v4.availability = 0
        v4.make = 'Toyota'
        v4.model = 'Prius'
        
        start_time = datetime.datetime.fromtimestamp(0)
        end_time = datetime.datetime.fromtimestamp(10000)
        
        view = AvailabilityHtmlView()
        
        # When...
        response_body = view.get_vehicle_availability(session, start_time, end_time, 
            [v1,v2,v3,v4], 'My Current Location')
        
        # Then...
        expected_body = \
"""<!DOCTYPE html>

<html>
  <head>
    <title>PhillyCarShare - Available Cars </title>
  </head>
  
  <body>
    
      
      
  
  <style>
    .available-vehicle {
      border: 1px solid green;
    }
    .unavailable-vehicle {
      border: 1px solid red;
    }
    .partially-available-vehicle {
      border: 1px solid yellow;
    }
  </style>
  
  <h1>Available Cars</h1>
  
  <div class="availability-options">
    <span>Showing cars near My Current Location</span>
    <span>from midnight Thu Jan 01 1970</span>
    <span>until 2:46 a.m. Thu Jan 01 1970</span>
  </div>
  
  
  
    <div class="available-pod">
      <div class="pod-name">Pod 1</div>
      
        
          <div class="available-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
            
          </div>
        </div>
      
        
          <div class="partially-available-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
              <span>Available at 1:06 a.m.</span>
            
            
          </div>
        </div>
      
        
          <div class="available-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
            
          </div>
        </div>
      
    </div>
  
    <div class="available-pod">
      <div class="pod-name">Pod 2</div>
      
        
          <div class="unavailabe-vehicle">
        
          
          <span>Toyota Prius</span>
          <div class="vehicle-stipulations">
            
            
          </div>
        </div>
      
    </div>
  
  

      
    
  </body>
</html>

"""
        response_body = response_body.replace('<','&lt;')
        response_body = response_body.replace('>','&gt;')
        expected_body = expected_body.replace('<','&lt;')
        expected_body = expected_body.replace('>','&gt;')
        
        self.assertEqual(response_body, expected_body)

