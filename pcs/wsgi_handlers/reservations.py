from pcs.wsgi_handlers.base import _SessionBasedHandler
from pcs.wsgi_handlers.base import _TimeRangeBasedHandler
from pcs.wsgi_handlers.base import WsgiParameterError
from pcs.fetchers.screenscrape.session import SessionScreenscrapeSource
from pcs.fetchers.screenscrape.reservations import ReservationsScreenscrapeSource
from pcs.renderers.json.error import ErrorJsonView
from pcs.renderers.json.reservations import ReservationsJsonView
from util.TimeZone import Eastern
from util.TimeZone import from_isostring

class ReservationsHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    def __init__(self,
                 session_source,
                 reservation_source,
                 reservation_view,
                 error_view):
        super(ReservationsHandler, self).__init__(session_source, error_view)
        
        self.reservation_source = reservation_source
        self.reservation_view = reservation_view
    
    def get_period(self):
        period = self.request.get('period', None)
        return from_isostring(period) if period else None
    
    def handle_get_reservations(self):
        try:
            userid = self.get_user_id()
            sessionid = self.get_session_id()
            
            period = self.get_period()
            
            session = self.session_source.get_existing_session(userid, sessionid)
            reservations, page, page_count = self.reservation_source.get_reservations(sessionid, period)
            response_body = self.reservation_view.render_reservations(session, reservations, page, page_count)
        
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


class ReservationsJsonHandler (ReservationsHandler):
    def __init__(self):
        super(ReservationsJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            ReservationsScreenscrapeSource(),
            ReservationsJsonView(),
            ErrorJsonView())

