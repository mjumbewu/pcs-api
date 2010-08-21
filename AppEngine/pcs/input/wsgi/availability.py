import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.source.screenscrape.login import LoginScreenscrapeSource
from pcs.view.html.availability import AvailabilityHtmlView

class AvailabilityHandler (webapp.RequestHandler):
    """
    Handles requests availability information
    """
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/my_reservations.php",
                 login_source=None,
                 availability_view=None):
        super(AvailabilityHandler, self).__init__()
        self.__host = host
        self.__path = path
        
        if login_source is not None:
            self.login_source = login_source
        else:
            self.login_source = LoginScreenscrapeSource()
        
        if availability_view is not None:
            self.availability_view = availability_view
        else:
            self.availability_view = AvailabilityHtmlView()
    
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
        session = self.login_source.get_existing_session(username, session_id)
        
        return session
    
    def get_available_vehicles(self, start_time, end_time):
        return []
        
    def get(self):
        session = self.get_session()
        
        import datetime
        start_time_str = self.request.get('start_time')
        end_time_str = self.request.get('end_time')
        
        start_time = datetime.datetime.fromtimestamp(int(start_time_str))
        end_time = datetime.datetime.fromtimestamp(int(end_time_str))
        
        vehicles = self.get_available_vehicles(start_time, end_time)
        
        response_body = self.availability_view.get_vehicle_availability(
            session, start_time, end_time, vehicles)
        
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        self.get()



application = webapp.WSGIApplication(
        [('/check_availability', AvailabilityHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
