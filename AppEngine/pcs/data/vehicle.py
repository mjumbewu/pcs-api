
class VehicleType (object):
#    model
#    info_url
#    img_url
#    amenities
    def __init__(self, vehicleid):
        self.id = vehicleid

class AvailableVehicle (object):
#    pod
#    vehicle
    def __init__(self, availableid):
        self.id = availableid

class Rate (object):
    def __init__(self, rateid):
        self.id = rateid

class PriceEstimate (object):
    # available_balance
    # available_credit
    # applied_credit
    # distance
    # hourly_rate
    # daily_rate
    # time_amount
    # distance_amount
    # tax_amount
    # fee_amount
    # total_amount
    # amount_due
    pass

