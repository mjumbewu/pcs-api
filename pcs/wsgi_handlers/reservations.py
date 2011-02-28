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
    
    def get_vehicle_id(self):
        vehicle_id = self.request.get('vehicle', None)
        if vehicle_id is None:
            raise WsgiParameterError('Could not find vehicle id.')
        return vehicle_id
    
    def get_reservation_memo(self):
        memo = self.request.get('memo', None)
        return memo
    
    def get(self):
        try:
            sessionid = self.get_session_id()
            period = self.get_period()
            
            session = None
            reservations, page, page_count = self.reservation_source.fetch_reservations(sessionid, period)
            response_body = self.reservation_view.render_reservations(session, reservations, page, page_count)
        
        except KeyError, e:
            response_body = self.generate_error(e)
            
        self.response.out.write(response_body);
        self.response.set_status(200);
    
    def post(self):
        try:
            sessionid = self.get_session_id()
            vehicleid = self.get_vehicle_id()
            start_time, end_time = self.get_time_range()
            memo = self.get_reservation_memo()
            
            session = None
            reservation = self.reservation_source.fetch_reservation_creation(
                sessionid, vehicleid, start_time, end_time, memo)
            
            response_body = self.reservation_view.render_confirmation(
                session, reservation, 'create')
            
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body);
        self.response.set_status(200)

class ReservationHandler (_SessionBasedHandler, _TimeRangeBasedHandler):
    def __init__(self,
                 session_source,
                 reservation_source,
                 reservation_view,
                 error_view):
        super(ReservationHandler, self).__init__(session_source, error_view)
        
        self.reservation_source = reservation_source
        self.reservation_view = reservation_view
    
    def get_reservation_memo(self):
        memo = self.request.get('memo', None)
        return memo
    
    def get_vehicle_id(self):
        vehicle_id = self.request.get('vehicle', None)
        if vehicle_id is None:
            raise WsgiParameterError('Could not find vehicle id.')
        return vehicle_id
    
    def get_mod_action(self):
        mod_action = self.request.get('action', None)
        if mod_action not in ('edit', 'early', 'extend'):
            raise WsgiParameterError('action parameter must be one of edit, early, or extend')
        return mod_action
    
    def get(self, liveid):
        try:
            sessionid = self.get_session_id()
            
            reservation = self.reservation_source.fetch_reservation_information(
                sessionid, liveid)
            
            session = None
            response_body = self.reservation_view.render_reservation(
                session, reservation)
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body)
        self.response.set_status(200)
    
    def put(self, liveid):
        try:
            sessionid = self.get_session_id()
            mod_type = self.get_mod_action()
            vehicleid = self.get_vehicle_id()
            start_time, end_time = self.get_time_range()
            memo = self.get_reservation_memo()
            
            reservation = self.reservation_source.fetch_reservation_modification(
                sessionid, mod_type, liveid, vehicleid, start_time, end_time, memo)
            
            session = None
            response_body = self.reservation_view.render_confirmation(
                session, reservation, 'modify')
        
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body)
        self.response.set_status(200)
    
    def delete(self, liveid):
        try:
            sessionid = self.get_session_id()
            vehicleid = self.get_vehicle_id()
            start_time, end_time = self.get_time_range()
            
            reservation = self.reservation_source.fetch_reservation_cancellation(
                sessionid, liveid, vehicleid, start_time, end_time)
            
            session = None
            response_body = self.reservation_view.render_confirmation(
                session, reservation, 'cancel')
            
        except Exception, e:
            response_body = self.generate_error(e)
        
        self.response.out.write(response_body)
        self.response.set_status(200)


class ReservationsJsonHandler (ReservationsHandler):
    def __init__(self):
        super(ReservationsJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            ReservationsScreenscrapeSource(),
            ReservationsJsonView(),
            ErrorJsonView())

class ReservationJsonHandler (ReservationHandler):
    def __init__(self):
        super(ReservationJsonHandler, self).__init__(
            SessionScreenscrapeSource(),
            ReservationsScreenscrapeSource(),
            ReservationsJsonView(),
            ErrorJsonView())

