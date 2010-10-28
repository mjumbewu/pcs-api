import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from pcs.data.session import Session
from pcs.fetchers import _SessionSourceInterface
from pcs.fetchers import SessionExpiredError
from pcs.fetchers import SessionLoginError
from pcs.fetchers.screenscrape import ScreenscrapeParseError
from pcs.fetchers.screenscrape.pcsconnection import PcsConnection
from util.abstract import override

class SessionScreenscrapeSource (_SessionSourceInterface):
    """
    Responsible for logging in and constructing a session from a screenscrape
    of a PhillyCarShare response.
    """
    SIMPLE_FAILURE_DOCUMENT = "<html><head><title>Please Login</title></head><body></body></html>"
    
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/index.php"):
        super(SessionScreenscrapeSource, self).__init__()
        self.__host = host
        self.__path = path
    
    def login_to_pcs(self, conn, userid, password):
        """
        Attempts to login to the given connection with the given userid and 
        password.
        
        @return: The server response  If login failed, the response
          body should be identifiable as an invalid session.
        """
        parameters = urllib.urlencode({
            'login[name]': userid,
            'login[password]': password})
        response = conn.request('https://' + self.__host + self.__path, "POST",
            parameters, {})
        
        return (response.read(), response.getheaders())
    
    def reconnect_to_pcs(self, conn, sessionid):
        """
        Attempts to load a session from the connection with the given session
        id.
        
        @return: The server response.  If reconnection failed, the response
          body should be identifiable as an invalid session.
        """
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        response = conn.request('http://' + self.__host + self.__path, "POST", 
            {}, headers)
        
        return (response.read(), response.getheaders())
    
    def body_is_valid_session(self, response_body):
        """
        Check the server response to see whether the login was sucessful.
        @return: Whether the connection was successful or not
        @raises: Exception if success of connection cannot be discerned
        """
        class LoginParser (htmlparserlib.HTMLParser):

            def __init__(self):
                htmlparserlib.HTMLParser.__init__(self)
                self.in_title = False
                self.title = ''
            
            def handle_starttag(self, tag, attrs):
                if tag.lower() == 'title':
                    self.in_title = True
            
            def handle_data(self, data):
                TRIGGER_TEXT = 'Please Login'
                if self.in_title:
                    self.title += data
            
            def handle_endtag(self, tag):
                if tag.lower() == 'title':
                    self.in_title = False
        
        parser = LoginParser()
        parser.feed(response_body)
        parser.close()
        
        if parser.title == 'Please Login':
            return False
        elif parser.title == 'My Message Manager': # First access after login
            return True
        elif parser.title == 'Reservation Manager': # Subsequent accesses
            return True
        else:
            raise ScreenscrapeParseError('Unknown session document title: %r' % parser.title)
    
    def create_session_from_login_response(self, suser, response_body, response_headers):
        cookie = cookielib.SimpleCookie()
        header_dict = dict(response_headers)
        cookie.load(header_dict.get('set-cookie'))
        
        parser = SessionHtmlParser()
        parser.feed(response_body)
        parser.close()
        return Session(cookie['sid'].value, suser, parser.fullname)
    
    def create_session_from_reconnect_response(self, suser, sid, response_body, response_headers):
        parser = SessionHtmlParser()
        parser.feed(response_body)
        parser.close()
        return Session(sid, suser, parser.fullname)
    
    def create_host_connection(self):
        conn = PcsConnection()
        return conn
    
    @override
    def create_session(self, userid, password):
        """
        @todo: Creating the connection here introduces a dependency for testing.
               It should be passed in as a parameter.  However, in practice, 
               creating it here has no effect on the tests.  It should be moved,
               but it is not a high priority.
        """
        conn = self.create_host_connection()
        
        pcs_login_body, pcs_login_headers = \
            self.login_to_pcs(conn, userid, password)
        self._body = pcs_login_body
        self._headers = pcs_login_headers
        
        if self.body_is_valid_session(pcs_login_body):
            return self.create_session_from_login_response(
                userid, pcs_login_body, pcs_login_headers)
        else:
            raise SessionLoginError('Incorrect user id/password combinantion.')
    
    @override
    def fetch_session(self, userid, sessionid):
        conn = self.create_host_connection()
        
        pcs_reconnect_body, pcs_reconnect_headers = \
            self.reconnect_to_pcs(conn, sessionid)
        self._body = pcs_reconnect_body
        self._headers = pcs_reconnect_headers
        
        if self.body_is_valid_session(pcs_reconnect_body):
            return self.create_session_from_reconnect_response(
                userid, sessionid, pcs_reconnect_body, pcs_reconnect_headers)
        else:
            raise SessionExpiredError('Your session has expired.')

class SessionParseError (Exception):
    pass

class SessionHtmlParser (htmlparserlib.HTMLParser):

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


