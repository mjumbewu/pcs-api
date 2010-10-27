
class Location (object):
    pass

class LocationProfile (Location):
    def __init__(self, profilename, profileid, profiledesc):
        self.name = profilename
        self.id = profileid
        self.desc = profiledesc

class LocationCoordinate (Location):
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
