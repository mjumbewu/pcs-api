import HTMLParser as htmlparserlib
import Cookie as cookielib

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
    
    @staticmethod
    def FromLoginResponse(suser, response_body, response_headers):
        cookie = cookielib.SimpleCookie()
        header_dict = dict(response_headers)
        cookie.load(header_dict.get('set-cookie'))
        
        parser = SessionParser()
        parser.feed(response_body)
        parser.close()
        return Session(cookie['sid'].value, suser, parser.fullname)
    
    @staticmethod
    def FromReconnectResponse(suser, sid, response_body, response_headers):
        parser = SessionParser()
        parser.feed(response_body)
        parser.close()
        return Session(sid, suser, parser.fullname)

class SessionParser (htmlparserlib.HTMLParser):

    def __init__(self):
        htmlparserlib.HTMLParser.__init__(self)
        self.in_p = False
        self.fullname = 'blah'
    
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'p':
            self.in_p = True
    
    def handle_data(self, data):
        TRIGGER_TEXT = ', you are signed in'
        if self.in_p and TRIGGER_TEXT in data:
            trigger_pos = data.find(TRIGGER_TEXT)
            self.fullname = data[:trigger_pos]
    
    def handle_endtag(self, tag):
        if tag.lower() == 'p':
            self.in_p = False


