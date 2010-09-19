import datetime

from util.TimeZone import Eastern

class ReservationStatus (object):
    CURRENT = 0
    UPCOMING = 1
    PAST = 2

class Reservation (object):
#    vehicle
#    pod
#    start_time
#    end_time
    def __init__(self, reservationid):
        self.id = reservationid
    
    @property
    def status(self):
        now = datetime.datetime.now(Eastern) - datetime.timedelta(days=4, hours=12)
        if now < self.start_time:
            return ReservationStatus.UPCOMING
        elif now > self.end_time:
            return ReservationStatus.PAST
        else:
            return ReservationStatus.CURRENT

