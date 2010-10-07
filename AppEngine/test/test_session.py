import unittest
import StringIO

from util.testing import Stub
from util.testing import patch

from pcs.source import SessionLoginError
from pcs.source import SessionExpiredError

from pcs.source.screenscrape.pcsconnection import PcsConnection
from pcs.source.screenscrape.session import SessionScreenscrapeSource
class SessionScreenscrapeSourceTest (unittest.TestCase):
    def testShouldThinkSessionDocumentIsValidIfTitleIsCorrect(self):
        """Login is successful if the response document has the correct title."""
        source = SessionScreenscrapeSource()
        document = "<html><head><title>My Message Manager</title></head><body></body></html>"
        
        is_valid = source.body_is_valid_session(document)
        
        self.assertEqual(is_valid, True)
    
    def testShouldThinkSessionDocumentIsInvalidIfTitleIsCorrect(self):
        """Login is failure if the response document has the correct title."""
        source = SessionScreenscrapeSource()
        document = "<html><head><title>Please Login</title></head><body></body></html>"
        
        is_valid = source.body_is_valid_session(document)
        
        self.assertEqual(is_valid, False)
    
    def testShouldCreateNoSessionIfLoginResultsInInvalidSessionDocument(self):
        """Expected session is returned from a failed login (expected session is None)."""
        source = SessionScreenscrapeSource()
        @patch(source)
        def login_to_pcs(self, conn, userid, password):
            return ("<html><head><title>Please Login</title></head><body></body></html>", {})
        
        try:
            session = source.get_new_session('uid', 'pass')
        
        except SessionLoginError:
            return
        
        self.fail('Should have raised SessionLoginError')
    
    def testShouldCreateNewSessionAccordingToContentInValidSessionDocument(self):
        """Expected session is returned from a successful login."""
        source = SessionScreenscrapeSource()
        @patch(source)
        def login_to_pcs(self, conn, userid, password):
            return ("""<html>
                  <head>
                    <title>My Message Manager</title>
                  </head>
                  <body>
                    <p>Mr. Bojangles, you are signed in. Yay!</p>
                  </body>
                </html>
             """,
             {'set-cookie':'sid=abcde'})
             
        session = source.get_new_session('uid', 'pass')
        
        self.assertEqual(session.id, 'abcde')
        self.assertEqual(session.user, 'uid')
        self.assertEqual(session.name, 'Mr. Bojangles')
    
    def testShouldKnowAboutASimpleInvalidSessionDocumentBody(self):
        """Screenscrape source should have a simple document that triggers login failure"""
        source = SessionScreenscrapeSource()
        document = SessionScreenscrapeSource.SIMPLE_FAILURE_DOCUMENT
        
        is_valid = source.body_is_valid_session(document)
        
        self.assert_(not is_valid)
    
    def testShouldReturnExpectedBodyTextFromConnectionWhenLoggingIn(self):
        """Logging in will get the expected response from the connection"""
        source = SessionScreenscrapeSource()
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                from StringIO import StringIO
                response = StringIO('Body Text')
                response.getheaders = lambda: {'h1':1,'h2':2}
                return response
        conn = StubConnection()
        
        body, headers = source.login_to_pcs(conn, 'uid', 'pass')
        
        self.assertEqual(body, 'Body Text')
        self.assertEqual(headers, {'h1':1,'h2':2})
    
    def testShouldSendCookiesToAndReturnExpectedBodyTextFromConnectionWhenReconnectingToSession(self):
        """Resuming session will get expected response from connection"""
        source = SessionScreenscrapeSource()
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.requestheaders = headers
                
                from StringIO import StringIO
                response = StringIO('Body Text')
                response.getheaders = lambda: {'h1':1,'h2':2}
                return response
        conn = StubConnection()
        
        body, headers = source.reconnect_to_pcs(conn, '1234567')
        
        self.assertEqual(conn.requestheaders, {'Cookie':'sid=1234567'})
        self.assertEqual(body, 'Body Text')
        self.assertEqual(headers, {'h1':1,'h2':2})
    
    def testShouldNotGetStuckOnTheCallToConnectionDotRequest(self):
        """Resuming session will get expected response from connection"""
        source = SessionScreenscrapeSource()
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.requestheaders = headers
                
                from StringIO import StringIO
                response = StringIO('Body Text')
                response.getheaders = lambda: {'h1':1,'h2':2}
                return response
        conn = StubConnection()
        
        body, headers = source.reconnect_to_pcs(conn, '1234567')
    
    def testShouldCreateNewSessionWhenGivenValidUserIdAndPassword(self):
        # Given...
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.requestheaders = headers
                
                from StringIO import StringIO
                response = StringIO('<html><head><title>My Message Manager</title></head><body><p>Jalani Bakari, you are signed in (Residential)!</body></html>')
                response.getheaders = lambda: {'set-cookie':'sid=12345abcde'}
                return response
        conn = StubConnection()
        
        source = SessionScreenscrapeSource()
        @patch(source)
        def create_host_connection(self):
            return conn
        
        # When...
        session = source.get_new_session('valid_user', 'valid_pass')
        
        # Then...
        self.assertEqual(session.user, 'valid_user')
        self.assertEqual(session.name, 'Jalani Bakari')
        self.assertEqual(session.id, '12345abcde')
    
    def testShouldRetrieveCurrentSessionWhenGivenValidSessionId(self):
        # Given...
        @Stub(PcsConnection)
        class StubConnection (object):
            def request(self, url, method, data, headers):
                self.requestheaders = headers
                
                from StringIO import StringIO
                response = StringIO('<html><head><title>Reservation Manager</title></head><body><p>Jalani Bakari, you are signed in (Residential)!</body></html>')
                response.getheaders = lambda: {}
                return response
        conn = StubConnection()
        
        source = SessionScreenscrapeSource()
        @patch(source)
        def create_host_connection(self):
            return conn
        
        # When...
        session = source.get_existing_session('valid_user', '12345abcde')
        
        # Then...
        self.assertEqual(session.user, 'valid_user')
        self.assertEqual(session.name, 'Jalani Bakari')
        self.assertEqual(session.id, '12345abcde')
    
    def testShouldRaiseErrorWhenRetrievingExistingSessionFails(self):
        # Given...
        source = SessionScreenscrapeSource()
        @patch(source)
        def reconnect_to_pcs(self, conn, sessionid):
            return ("<html><head><title>Please Login</title></head><body></body></html>", {})
        
        # When...
        try:
            session = source.get_existing_session('valid_user', 'expiredsession12345abcde')
        
        # Then...
        except SessionExpiredError:
            return
        
        self.fail('Should have raised SessionExpiredError')

from pcs.input.wsgi.session import SessionHandler
from pcs.source import _SessionSourceInterface
from pcs.view import _SessionViewInterface
from pcs.source import SessionLoginError
class SessionHandlerTest (unittest.TestCase):
    def setUp(self):
        class StubRequest (dict):
            cookies = {}
        
        class StubHeaders (object):
            header_list = []
            def add_header(self, key, val):
                self.header_list.append((key,val))
        
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
            headers = StubHeaders()
        
        @Stub(_SessionSourceInterface)
        class StubSessionSource (object):
            pass
        
        @Stub(_SessionViewInterface)
        class StubSessionView (object):
            def get_session_overview(self, session):
                self.session = session
                return 'Session'
        
        class StubErrorView (object):
            def get_error(self, error_code, error_msg):
                return 'No Session'
        
        self.session_view = StubSessionView()
        self.session_source = StubSessionSource()
        self.error_view = StubErrorView()
        
        # System under test
        self.handler = SessionHandler(self.session_source, self.session_view, self.error_view)
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
    
    def testShouldReturnGivenUsernameAndPasswordAsCredentials(self):
        # Given...
        self.handler.request['username'] = 'uname'
        self.handler.request['password'] = 'pword'
        
        # When...
        uname, pword = self.handler.get_credentials()
        
        # Then...
        self.assertEqual(uname, 'uname')
        self.assertEqual(pword, 'pword')
    
    def testShouldCreateNewSessionFromValidUsernameAndPassword(self):
        @patch(self.session_source)
        def get_new_session(self, userid, password):
            if userid == 'uname' and password == 'pword':
                return 'my session'
            else:
                raise SessionLoginError()
        
        uname = 'uname'
        pword = 'pword'
        
        session = self.handler.get_new_session(uname, pword)
        
        self.assertEqual(session, 'my session')
    
    def testShouldRaiseErrorWhenGivenInvalidUsernamePasswordCombination(self):
        @patch(self.session_source)
        def get_new_session(self, userid, password):
            if userid == 'uname' and password == 'pword':
                return 'my session'
            else:
                raise SessionLoginError()
        
        uname = 'uname'
        pword = 'wrong_pword'
        
        try:
            session = self.handler.get_new_session(uname, pword)
        
        except SessionLoginError:
            return
        
        self.fail('Should have raised error for user %r and pass %r' % (uname, pword))
    
    def testShouldRespondWithSuccessContentWhenSessionIdIsRecognized(self):
        # Given...
        @patch(self.handler)
        def get_user_id(self):
            self.userid_called = True
            return 'user1234'
        
        @patch(self.handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(self.handler)
        def get_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            return 'my session'
        
        @patch(self.session_view)
        def get_session_overview(self, session):
            self.session = session
            return 'session overview body'
        
        # When...
        self.handler.get()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assert_(self.handler.userid_called)
        self.assert_(self.handler.sessionid_called)
        self.assertEqual(self.handler.userid, 'user1234')
        self.assertEqual(self.handler.sessionid, 'ses1234')
        self.assertEqual(self.session_view.session, 'my session')
        self.assertEqual(response_body, 'session overview body')
    
    def testShouldRespondWithFailureContentWhenSessionIdIsNotRecognized(self):
        # Given...
        @patch(self.handler)
        def get_user_id(self):
            self.userid_called = True
            return 'user1234'
        
        @patch(self.handler)
        def get_session_id(self):
            self.sessionid_called = True
            return 'ses1234'
        
        @patch(self.handler)
        def get_session(self, userid, sessionid):
            self.userid = userid
            self.sessionid = sessionid
            raise SessionExpiredError()
        
        @patch(self.error_view)
        def get_error(self, error_code, error_msg):
            return error_msg
        
        # When...
        self.handler.get()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assert_(self.handler.userid_called)
        self.assert_(self.handler.sessionid_called)
        self.assertEqual(self.handler.userid, 'user1234')
        self.assertEqual(self.handler.sessionid, 'ses1234')
        self.assert_(response_body.startswith('SessionExpiredError'), 'Response does not start with SessionExpiredError: %r' % response_body)
    
    def testShouldSaveSessionToSetCookieHeader(self):
        class StubSession (object):
            id = 'ses1234'
            user = 'user1234'
            name = 'My User Name'
        session = StubSession()
        
        self.handler.save_session(session)
        
        self.assertEqual(self.handler.response.headers.header_list, 
            [ ('Set-Cookie','sid=ses1234; path=/'), 
              ('Set-Cookie','suser=user1234; path=/'),
              ('Set-Cookie','sname=My User Name; path=/') ])
    
    def testShouldRespondWithSuccessContentWhenUserIdAndPasswordAreRecognized(self):
        # Given...
        @patch(self.handler)
        def get_credentials(self):
            self.credentials_called = True
            return 'user1234', 'pass1234'
        
        @patch(self.handler)
        def get_new_session(self, userid, password):
            self.userid = userid
            self.password = password
            return 'my session'
        
        @patch(self.session_view)
        def get_session_overview(self, session):
            self.session = session
            return 'session overview body'
        
        @patch(self.handler)
        def save_session(self, session):
            self.session = session
        
        # When...
        self.handler.post()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assert_(self.handler.credentials_called)
        self.assertEqual(self.handler.userid, 'user1234')
        self.assertEqual(self.handler.password, 'pass1234')
        self.assertEqual(self.session_view.session, 'my session')
        self.assertEqual(self.handler.session, 'my session')
        self.assertEqual(response_body, 'session overview body')
    
    def testShouldRespondWithFailureContentWhenUserIdAndPasswordAreNotRecognized(self):
        # Given...
        @patch(self.handler)
        def get_credentials(self):
            self.credentials_called = True
            return 'user1234', 'pass1234'
        
        @patch(self.handler)
        def get_new_session(self, userid, password):
            self.userid = userid
            self.password = password
            raise SessionLoginError()
        
        @patch(self.error_view)
        def get_error(self, error_code, error_msg):
            return error_msg
        
        # When...
        self.handler.post()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assert_(self.handler.credentials_called)
        self.assertEqual(self.handler.userid, 'user1234')
        self.assertEqual(self.handler.password, 'pass1234')
        self.assert_(response_body.startswith('SessionLoginError'), 'Response does not start with SessionLoginError: %r' % response_body)

from pcs.data.session import Session
from pcs.view.json.session import SessionJsonView
class SessionJsonViewTest (unittest.TestCase):
		def testShouldReturnAppropriateBodyWhenSessionIsNone(self):
				expected = \
"""{"session" : {

	"is_valid" : false,
	"error" : ""

}}"""
				view = SessionJsonView()
				
				result = view.get_session_overview(None)
				self.assertEqual(result, expected)
		
		def testShouldReturnAppropriateBodyWithValidSession(self):
				expected = \
"""{"session" : {

	"is_valid" : true,
	"id" : "ses123",
	"userid" : "user123",
	"name" : "user name"

}}"""
				view = SessionJsonView()
				session = Session('ses123', 'user123', 'user name')
				
				result = view.get_session_overview(session)
				self.assertEqual(result, expected)
				
				
from pcs.input.wsgi.session import SessionHtmlHandler
from pcs.view.html.session import SessionHtmlView
from pcs.view.html.error import ErrorHtmlView
class SessionHtmlHandlerTest (unittest.TestCase):
    def testShouldBeInitializedWithASessionHtmlView(self):
        handler = SessionHtmlHandler()
        
        self.assertEqual(handler.session_view.__class__.__name__, SessionHtmlView.__name__)
        self.assertEqual(handler.session_source.__class__.__name__, SessionScreenscrapeSource.__name__)
        self.assertEqual(handler.error_view.__class__.__name__, ErrorHtmlView.__name__)

#from pcs.input.wsgi.session import SessionJsonHandler
#from pcs.view.json.session import SessionJsonView
#from pcs.view.json.error import ErrorJsonView
#class SessionJsonHandlerTest (unittest.TestCase):
#    def testShouldBeInitializedWithASessionJsonView(self):
#        handler = SessionJsonHandler()
#        
#        self.assertEqual(handler.session_view.__class__.__name__, SessionJsonView.__name__)
#        self.assertEqual(handler.session_source.__class__.__name__, SessionScreenscrapeSource.__name__)
#        self.assertEqual(handler.error_view.__class__.__name__, ErrorJsonView.__name__)
