import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.source.screenscrape.availability import AvailabilityScreenscrapeSource
from pcs.view.html.availability import AvailabilityHtmlView

class AvailabilityHandler (webapp.RequestHandler):
    """
    Handles requests availability information
    """
    def __init__(self,
                 session_source,
                 availability_source,
                 availability_view):
        super(AvailabilityHandler, self).__init__()
        
        self.session_source = session_source
        self.availability_view = availability_view
    
    def get_session_id(self):
        username = self.request.cookies.get('suser', None)
        session_id = self.request.cookies.get('sid', None)
        
        return username, session_id
    
    def get_session(self):
        """
        Attempt to get a session using username and password credentials. If no
        password is available, attempt to find an existing session id to use.
        @return: A valid session or None
        """
        username, session_id = self.get_session_id()
        session = self.session_source.get_existing_session(username, session_id)
        
        return session
    
    def get_available_vehicles(self, start_time, end_time):
        # This is a stub
        return []
    
    def get_location(self):
        # This is a stub
        'My Current Location'
    
    def get_time_range(self):
        import datetime
        start_time_str = self.request.get('start_time')
        end_time_str = self.request.get('end_time')
        
        now_time = datetime.datetime.now()
        if start_time_str:
            start_time = datetime.datetime.fromtimestamp(int(start_time_str))
        else:
            start_time = now_time
        
        if end_time_str:
            end_time = datetime.datetime.fromtimestamp(int(end_time_str))
        else:
            end_time = now_time + datetime.timedelta(hours=3)
        
        return start_time, end_time
        
        
    def get(self):
        session = self.get_session()
        start_time, end_time = self.get_time_range()
        location = self.get_location()
        vehicles = self.get_available_vehicles(start_time, end_time)
        
        response_body = self.availability_view.get_vehicle_availability(
            session, start_time, end_time, vehicles, location)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()

class AvailabilityHtmlHandler (AvailabilityHandler):
    def __init__(self):
        super(AvailabilityHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            AvailabilityScreenscrapeSource(),
            AvailabilityHtmlView())
    


application = webapp.WSGIApplication(
        [('/availability.html', AvailabilityHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
