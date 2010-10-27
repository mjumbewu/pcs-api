
class Session (object):
    
    def __init__(self, sessionid, username, fullname, headers={}):
        self.id = sessionid
        self.user = username
        self.name = fullname
        self.headers = headers
    
    @staticmethod
    def FromRequest(request):
        sid = request.cookies['sid']
        suser = request.cookies['suser']
        sname = request.cookies['sname']
        return Session(sid, suser, sname)
    

