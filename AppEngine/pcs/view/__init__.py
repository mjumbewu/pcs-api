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
    def get_vehicle_availability(self, session, start_time, end_time, vehicles, location):
        raise NotImplementedError()

class _ErrorViewInterface (object):
    def get_error(self, error_code, error_msg):
        raise NotImplementedError()
