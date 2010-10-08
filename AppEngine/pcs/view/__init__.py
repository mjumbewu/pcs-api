"""This package is for objects that handle formatting data for consumption by a user or by any other system.  Views may be in HTML, JSON, XML, or whatever."""

class _LoginViewInterface (object):
    def get_login_form(self, userid):
        raise NotImplementedError()

class _SessionViewInterface (object):
    def get_session_overview(self, session):
        raise NotImplementedError()

class _LocationsViewInterface (object):
    def get_locations(self, session, locations):
        raise NotImplementedError()
    
class _AvailabilityViewInterface (object):
    def render_location_availability(self, session, location, start_time, end_time, vehicles):
        raise NotImplementedError()
    
    def render_vehicle_availability(self, session, vehicle, start_time, end_time, price):
        raise NotImplementedError()

class _ReservationsViewInterface (object):
    def get_reservations(self, session, reservations):
        raise NotImplementedError()
    
    def get_successful_new_reservation(self, session, reservation):
        raise NotImplementedError()

class _ErrorViewInterface (object):
    def get_error(self, error_code, error_msg):
        raise NotImplementedError()
