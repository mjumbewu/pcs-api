"""This package is for objects that handle retrieving information from PhillyCarShare and storing that information in this project's data model.  For now the primary source package uses screenscraping, but who knows, PhillyCarShare may employ a public-facing API at some point."""

class _SourceBase (object):
    pass

class _SessionSourceInterface (object):
    def create_session(self, userid, password):
        raise NotImplementedError()
    
    def fetch_session(self, userid, sessionid):
        raise NotImplementedError()

class _AvailabilitySourceInterface (object):
    def fetch_available_vehicles_near(self, sessionid, locationid, start_time, end_time):
        raise NotImplementedError()
    
    def fetch_vehicle_availability(self, sessionid, vehicleid, start_time, end_time):
        raise NotImplementedError()
    
    def fetch_vehicle_price_estimate(self, sessionid, vehicleid, start_time, end_time):
        raise NotImplementedError()
    
    def fetch_updated_transaction(self, sessionid, vehicleid, start_time, end_time):
        raise NotImplementedError()

class _ReservationsSourceInterface (object):
    def fetch_reservations(self, sessionid, year_month=None):
        raise NotImplementedError()
    
    def fetch_reservation_creation(self, sessionid, vehicleid, start_time, end_time, reservation_memo):
        raise NotImplementedError()
    
    def fetch_reservation_modification(self, sessionid, mod_type, liveid, vehicleid, start_time, end_time, reservation_memo):
        raise NotImplementedError()
    
    def fetch_reservation_cancellation(self, sessionid, liveid, vehicleid, start_time, end_time):
        raise NotImplementedError()
    
    def fetch_reservation_information(self, sessionid, liveid):
        raise NotImplementedError()

class _LocationsSourceInterface (object):
    def fetch_location_profiles(self, sessionid):
        raise NotImplementedError()
    
    def fetch_location_profile(self, sessionid, locationid):
        raise NotImplementedError()
    
    def fetch_custom_location(self, location_name, location_key):
        raise NotImplementedError()

class SessionLoginError (Exception):
    pass

class SessionExpiredError (Exception):
    pass
