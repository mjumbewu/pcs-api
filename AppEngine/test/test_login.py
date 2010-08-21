import unittest

from pcs.source.screenscrape.session import SessionScreenscrapeSource
class SessionScreenscrapeSourceTest (unittest.TestCase):
    def test1(self):
        """Login is successful if the response document has the correct title."""
        source = SessionScreenscrapeSource()
        document = "<html><head><title>My Message Manager</title></head><body></body></html>"
        self.assertEqual(source.body_is_valid_session(document), True)
    
    def test2(self):
        """Login is failure if the response document has the correct title."""
        source = SessionScreenscrapeSource()
        document = "<html><head><title>Please Login</title></head><body></body></html>"
        self.assertEqual(source.body_is_valid_session(document), False)
    
    def test3(self):
        """Expected session is returned from a failed login (expected session is None)."""
        source = SessionScreenscrapeSource()
        source.login_to_pcs = lambda conn, username, password: \
            ("<html><head><title>Please Login</title></head><body></body></html>", {})
        session = source.get_new_session('uid', 'pass')
        self.assert_(session is None)
    
    def test4(self):
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
    
    def test5(self):
        """Screenscrape source should have a simple document that triggers login failure"""
        source = SessionScreenscrapeSource()
        document = SessionScreenscrapeSource.SIMPLE_FAILURE_DOCUMENT
        self.assert_(not source.body_is_valid_session(document))
    
    def test6(self):
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
    
    def test7(self):
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
