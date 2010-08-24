"""This package is for objects that handle retrieving information from PhillyCarShare and storing that information in this project's data model.  For now the primary source package uses screenscraping, but who knows, PhillyCarShare may employ a public-facing API at some point."""

class _SourceBase (object):
    pass

class _SessionSourceInterface (object):
    def get_new_session(self, userid, password):
        raise NotImplementedError()
    
    def get_existing_session(self, userid, sessionid):
        raise NotImplementedError()

class _AvailabilitySourceInterface (object):
    def get_available_vehicles_near(self, sessionid, location, start_time, end_time):
        raise NotImplementedError()
