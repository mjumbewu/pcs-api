from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.input.wsgi import _SessionBasedHandler
from pcs.input.wsgi import _TimeRangeBasedHandler
from pcs.input.wsgi import WsgiParameterError
from pcs.source.screenscrape.session import SessionScreenscrapeSource
from pcs.source.screenscrape.reservations import ReservationsScreenscrapeSource
from pcs.view.html.error import ErrorHtmlView
from pcs.view.html.reservations import ReservationsHtmlView
from pcs.view.json.error import ErrorJsonView
from pcs.view.json.reservations import ReservationsJsonView
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
    
    def get_year(self):
        year = self.request.get('year', None)
        return int(year) if year else None
    
    def get_month(self):
        month = self.request.get('month', None)
        return int(month) if month else None
    
    def handle_get_reservations(self):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            
            year = self.get_year()
            month = self.get_month()
            
            if year is None or month is None:
                year_month = None
            else:
                year_month = (year, month)
            
            session = self.session_source.get_existing_session(userid, sessionid)
            reservations = self.reservation_source.get_reservations(sessionid, year_month)
            response_body = self.reservation_view.render_reservations(session, reservations)
        
        except KeyError, e:
            response_body = self.generate_error(e)
            
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def get_vehicle_id(self):
        vehicle_id = self.request.get('vehicle', None)
        if vehicle_id is None:
            raise WsgiParameterError('Could not find vehicle id.')
        return vehicle_id
    
    def get_reservation_memo(self):
        return 'new reservation'
    
    def get_transaction_id(self):
        transaction_id = self.request.get('transaction', None)
        if transaction_id is None:
            raise WsgiParameterError('Could not find transaction id.')
        return transaction_id
    
    def handle_create_reservation(self):
        try:
            userid =  self.get_user_id()
            sessionid = self.get_session_id()
            vehicleid = self.get_vehicle_id()
            transactionid = self.get_transaction_id()
            start_time, end_time = self.get_time_range()
            memo = self.get_reservation_memo()
            
            session = self.session_source.get_existing_session(userid, sessionid)
            reservation = self.reservation_source.get_new_reservation(sessionid, vehicleid, transactionid, start_time, end_time, memo)
            if reservation:
                response_body = \
                    self.reservation_view.get_successful_new_reservation(
                        session, reservation)
            else:
                response_body = \
                    self.reservation_view.get_failed_new_reservation(
                        session, start_time, end_time)
            
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200)
    
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
        super(ReservationHandler, self).__init__(session_source, error_view)
        
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

class ReservationEditorHtmlHandler (_TimeRangeBasedHandler):
    def get(self, reservationid):
        import os
        from google.appengine.ext.webapp import template
        from util.TimeZone import to_xchange_time
        
        start_time, end_time = self.get_time_range()
        status = self.request.get('status')
        
        values = {
            'session': 'valid',
            'reservationid': reservationid,
            'start_time': start_time,
            'start_stamp': to_xchange_time(start_time),
            'end_time': end_time,
            'end_stamp': to_xchange_time(end_time),
            'status': status
        }
        
        path = os.path.join(os.path.dirname(__file__), '../../view/html/reservation-editor.html')
        response_body = template.render(path, values)
        self.response.out.write(response_body)

class ReservationsJsonHandler (ReservationsHandler):
    def __init__(self):
        super(ReservationsJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            ReservationsScreenscrapeSource(),
            ReservationsJsonView(),
            ErrorJsonView())


application = webapp.WSGIApplication(
        [('/reservations.html', ReservationsHtmlHandler),
         ('/reservations.json', ReservationsJsonHandler),
         ('/reservations/([.^/]*).html', ReservationHtmlHandler),
         ('/reservations/(.*)/editor.html', ReservationEditorHtmlHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
