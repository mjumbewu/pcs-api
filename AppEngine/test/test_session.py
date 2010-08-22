import unittest
import StringIO

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
        source.login_to_pcs = lambda conn, username, password: \
            ("<html><head><title>Please Login</title></head><body></body></html>", {})
            
        session = source.get_new_session('uid', 'pass')
        
        self.assert_(session is None)
    
    def testShouldCreateNewSessionAccordingToContentInValidSessionDocument(self):
        """Expected session is returned from a successful login."""
        source = SessionScreenscrapeSource()
        source.login_to_pcs = lambda conn, username, password: \
            ("""<html>
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
        class StubConnection (object):
            def request(self, method, path, data='', headers={}):
                pass
            def getresponse(self):
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
        class StubConnection (object):
            def request(self, method, path, data='', headers={}):
                self.requestheaders = headers
            def getresponse(self):
                from StringIO import StringIO
                response = StringIO('Body Text')
                response.getheaders = lambda: {'h1':1,'h2':2}
                return response
        conn = StubConnection()
        
        body, headers = source.reconnect_to_pcs(conn, '1234567')
        
        self.assertEqual(conn.requestheaders, {'Cookie':'sid=1234567'})
        self.assertEqual(body, 'Body Text')
        self.assertEqual(headers, {'h1':1,'h2':2})

from pcs.input.wsgi.session import SessionHandler
class SessionHandlerTest (unittest.TestCase):
    def setUp(self):
        class StubRequest (dict):
            cookies = {}
        
        class StubHeaders (object):
            headers = []
            def add_header(self, key, val):
                self.headers.append((key,val))
        
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
            headers = StubHeaders()
        
        class StubSessionSource (object):
            _body = ''
            
            def get_existing_session(self, userid, sessionid):
                return None
            def get_new_session(self, userid, password):
                if userid == 'uname' and password == 'pword':
                    class StubSession (object):
                        id = '5b'
                        user = 'uname'
                        name = 'My Name'
                    return StubSession()
                else:
                    return None
        
        class StubSessionView (object):
            def get_session_overview(self, session):
                if session:
                    return 'Session'
                else:
                    return 'No Session'
        
        # System under test
        self.handler = SessionHandler(StubSessionSource(), StubSessionView())
        self.handler.request = StubRequest()
        self.handler.response = StubResponse()
    
    def testShouldRespondWithSuccessContentWhenUserIdAndPasswordAreRecognized(self):
        # Given...
        self.handler.request['username'] = 'uname'
        self.handler.request['password'] = 'pword'
        
        # When...
        self.handler.get()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assertEqual(response_body, 'Session')
    
    def testShouldRespondWithFailureContentWhenUserIdAndPasswordAreNotRecognized(self):
        # Given...
        self.handler.request['username'] = 'uname'
        self.handler.request['password'] = 'pword1'
        
        # When...
        self.handler.get()
        
        # Then...
        response_body = self.handler.response.out.getvalue()
        self.assertEqual(response_body, 'No Session')

from pcs.input.wsgi.session import SessionHtmlHandler
from pcs.view.html.session import SessionHtmlView
class SessionHtmlHandlerTest (unittest.TestCase):
    def testShouldBeInitializedWithASessionHtmlView(self):
        handler = SessionHtmlHandler()
        
        self.assertEqual(handler.session_view.__class__.__name__, SessionHtmlView.__name__)
        self.assertEqual(handler.session_source.__class__.__name__, SessionScreenscrapeSource.__name__)
        
