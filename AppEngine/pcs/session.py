class Session (object):
    
    def __init__(self, sessionid):
        self.id = sessionid
    
    def get_new_reservation_url(self):
        return "/newreservation"
    
    def get_existing_reservations_url(self):
        return "http://reservations.phillycarshare.org/my_reservations.php?mv_action=main&_r=1&sid=" + self.id
    
    def get_messages_url(self):
        return "http://reservations.phillycarshare.org/my_messages.php?_r=1&sid=" + self.id
    
    def get_account_info_url(self):
        return "http://reservations.phillycarshare.org/my_info.php?_r=1&sid=" + self.id
    
    def get_feedback_url(self):
        return "http://reservations.phillycarshare.org/my_problems.php?_r=1&sid=" + self.id
    
    @staticmethod
    def FromRequest(request):
        sid = request.cookies['sid']
        return Session(sid)

