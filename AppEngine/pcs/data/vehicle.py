
class VehicleModel (object):
#    name
#    info_url
#    img_url
#    amenities
    def __init__(self, modelid=None):
        self.id = modelid

class Vehicle (object):
#    pod
#    model
#    rate
    def __init__(self, vehicleid):
        self.id = vehicleid

class AvailableVehicle (object):
#    vehicle
#    start_time
#    end_time
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

