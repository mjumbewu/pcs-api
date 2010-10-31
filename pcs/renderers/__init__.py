"""This package is for objects that handle formatting data for consumption by a user or by any other system.  Views may be in HTML, JSON, XML, or whatever."""

class _LoginViewInterface (object):
    def get_login_form(self, userid):
        raise NotImplementedError()

class _SessionViewInterface (object):
    def render_session(self, session):
        raise NotImplementedError()

class _LocationsViewInterface (object):
    def render_locations(self, session, locations):
        raise NotImplementedError()
    
class _AvailabilityViewInterface (object):
    def render_location_availability(self, session, location, start_time, end_time, vehicle_availabilities):
        raise NotImplementedError()
    
    def render_vehicle_availability(self, session, vehicle, start_time, end_time, price):
        raise NotImplementedError()

class _ReservationsViewInterface (object):
    def render_reservations(self, session, reservations, page_num, total_pages):
        raise NotImplementedError()
    
    def render_confirmation(self, session, reservation, event):
        raise NotImplementedError()

class _ErrorViewInterface (object):
    def render_error(self, error_code, error_msg, error_detail):
        raise NotImplementedError()
