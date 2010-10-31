import datetime

from util.TimeZone import Eastern

class ReservationStatus (object):
    CURRENT = 0
    UPCOMING = 1
    PAST = 2

class ReservationEvent (object):
    CREATION = 'create'
    MODIFICATION = 'modify'
    CANCELLATION = 'cancel'

class Reservation (object):
#    vehicle
#    pod
#    start_time
#    end_time
    def __init__(self, logid, liveid=None):
        """
        Past reservations have log ids, but no LIVE ids. When you request a list
        of reservations, you're actually requesting your reservation LOG. Only
        current and upcoming reservations have a live id. The log id is what PCS
        calls a confirmation id. The live id is the reservation id (according to
        PCS). This live reservation id is what would be passed to the API to
        modify or cancel a reservation. There will be no concept of getting a
        single reservation in the API. It just doesn't make sense to support
        right now. If PCS opens an API in the future, maybe it can be added. For
        now, it's unnecessary.
        """
        
        self.logid = logid
        self.liveid = liveid
    
    @property
    def status(self):
        now = datetime.datetime.now(Eastern) - datetime.timedelta(days=4, hours=12)
        if now < self.start_time:
            return ReservationStatus.UPCOMING
        elif now > self.end_time:
            return ReservationStatus.PAST
        else:
            return ReservationStatus.CURRENT

