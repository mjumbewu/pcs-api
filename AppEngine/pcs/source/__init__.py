"""This package is for objects that handle retrieving information from PhillyCarShare and storing that information in this project's data model.  For now the primary source package uses screenscraping, but who knows, PhillyCarShare may employ a public-facing API at some point."""

class _SourceBase (object):
    pass

class _SessionSourceInterface (object):
    def get_new_session(self, userid, password):
        raise NotImplementedError()
    
    def get_existing_session(self, userid, sessionid):
        raise NotImplementedError()

class _AvailabilitySourceInterface (object):
    def get_available_vehicles_near(self, sessionid, locationid, start_time, end_time):
        raise NotImplementedError()
    
    def get_vehicle(self, sessionid, vehicleid, start_time, end_time):
        raise NotImplementedError()
    
    def get_vehicle_price_estimate(self, sessionid, vehicleid, start_time, end_time):
        raise NotImplementedError()

class _LocationsSourceInterface (object):
    def get_location_profiles(self, sessionid):
        raise NotImplementedError()
    
    def get_location_profile(self, sessionid, locationid):
        raise NotImplementedError()
    
    def get_custom_location(self, location_name, location_key):
        raise NotImplementedError()

class SessionLoginError (Exception):
    pass

class SessionExpiredError (Exception):
    pass
