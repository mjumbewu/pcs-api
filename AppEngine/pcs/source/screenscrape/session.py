import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

from pcs.data.session import Session

class SessionScreenscrapeSource (object):
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
    
    def login_to_pcs(self, conn, username, password):
        """
        Attempts to login to the given connection with the given username and 
        password.
        
        @return: The server response  If login failed, the response
          body should be identifiable as an invalid session.
        """
        parameters = urllib.urlencode({
            'login[name]': username,
            'login[password]': password})
        conn.request("POST", self.__path,
            parameters)
        conn._follow_redirects = True
        
        try:
            response = conn.getresponse()
        except:
            return (self.SIMPLE_FAILURE_DOCUMENT, [])
        
        return (response.read(), response.getheaders())
    
    def reconnect_to_pcs(self, conn, session_id):
        """
        Attempts to load a session from the connection with the given session
        id.
        
        @return: The server response.  If reconnection failed, the response
          body should be identifiable as an invalid session.
        """
        headers = {
            'Cookie': 'sid=%s' % session_id}
        conn.request("POST", self.__path,
            {}, headers)
        conn._follow_redirects = True
        
        try:
            response = conn.getresponse()
        except:
            return (self.SIMPLE_FAILURE_DOCUMENT, [])
        
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
        elif parser.title == 'Reservation Manager': # Subsequent accesss
            return True
        else:
            raise Exception('Unknown Login Title: %r' % parser.title)
    
    def get_new_session(self, username, password):
        """
        @todo: Creating the connection here introduces a dependency for testing.
               It should be passed in as a parameter.  However, in practice, 
               creating it here has no effect on the tests.  It should be moved,
               but it is not a high priority.
        """
        conn = httplib.HTTPSConnection(self.__host)
        
        pcs_login_body, pcs_login_headers = \
            self.login_to_pcs(conn, username, password)
        self._body = pcs_login_body
        self._headers = pcs_login_headers
        
        if self.body_is_valid_session(pcs_login_body):
            return Session.FromLoginResponse(username, pcs_login_body, 
                                             pcs_login_headers)
        else:
            return None
    
    def get_existing_session(self, username, session_id):
        conn = httplib.HTTPSConnection(self.__host)
        
        pcs_reconnect_body, pcs_reconnect_headers = \
            self.reconnect_to_pcs(conn, session_id)
        self._body = pcs_reconnect_body
        self._headers = pcs_reconnect_headers
        
        if self.body_is_valid_session(pcs_reconnect_body):
            return Session.FromReconnectResponse(username, session_id,
                                                 pcs_reconnect_body, 
                                                 pcs_reconnect_headers)
        else:
            return None

