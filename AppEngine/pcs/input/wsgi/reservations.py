from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.input.wsgi import _SessionBasedHandler
from pcs.input.wsgi import _TimeRangeBasedHandler
from pcs.input.wsgi import WsgiParameterError
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.view.html.error import ErrorHtmlView
from util.TimeZone import Eastern

class ReservationsHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    def __init__(self,
                 session_source,
                 reservation_source,
                 reservation_view,
                 error_view):
        super(ReservationsHandler, self).__init__(session_source, error_view)
        
        self.reservation_source = reservation_source
        self.reservation_view = reservation_view
    
    def handle_get_reservations(self):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            
            session = self.session_source.get_existing_session(userid, sessionid)
            reservations = self.reservation_source.get_reservations(sessionid)
            response_body = self.reservation_view.get_reservations(session, reservations)
        
        except KeyError, e:
            response_body = self.generate_error(e)
            
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def get(self):
        self.handle_get_reservations()
    
    def post(self):
        self.handle_create_reservation()

class ReservationHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    def __init__(self,
                 session_source,
                 reservation_source,
                 reservation_view,
                 error_view):
        super(ReservationsHandler, self).__init__(session_source, error_view)
        
        self.reservation_source = reservation_source
        self.reservation_view = reservation_view
    
    def get(self, reservationid):
        self.handle_get_reservation(reservationid)
    
    def put(self, reservationid):
        self.handle_edit_reservation(reservationid)
    
    def delete(self, reservationid):
        self.handle_cancel_reservation(reservationid)


class ReservationsHtmlHandler (ReservationsHandler):
    def __init__(self):
        super(ReservationsHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            ReservationsScreenscrapeSource(),
            ReservationsHtmlView(),
            ErrorHtmlView())

class ReservationHtmlHandler (ReservationHandler):
    def __init__(self):
        super(ReservationHtmlHandler, self).__init__(
            SessionScreenscrapeSource(),
            ReservationsScreenscrapeSource(),
            ReservationsHtmlView(),
            ErrorHtmlView())
            

application = webapp.WSGIApplication(
        [('/reservations.html', ReservationsHtmlHandler),
         ('/reservations/(.*).html', ReservationHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
