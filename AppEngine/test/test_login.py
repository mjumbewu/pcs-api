import unittest

from pcs.source.screenscrape.login import LoginScreenscrapeSource
class login_screenscrape_TestCase (unittest.TestCase):
    def test1(self):
        """Login is successful if the response document has the correct title."""
        source = LoginScreenscrapeSource()
        document = "<html><head><title>My Message Manager</title></head><body></body></html>"
        self.assertEqual(source.login_was_successful(document), True)
    
    def test2(self):
        """Login is failure if the response document has the correct title."""
        source = LoginScreenscrapeSource()
        document = "<html><head><title>Please Login</title></head><body></body></html>"
        self.assertEqual(source.login_was_successful(document), False)
    
    def test3(self):
        """Expected session is returned from a failed login (expected session is None)."""
        source = LoginScreenscrapeSource()
        source.login_to_pcs = lambda conn, username, password: \
            ("<html><head><title>Please Login</title></head><body></body></html>", {})
        session = source.get_new_session('uid', 'pass')
        self.assert_(session is None)
    
    def test4(self):
        """Expected session is returned from a successful login."""
        source = LoginScreenscrapeSource()
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
        source = LoginScreenscrapeSource()
        document = LoginScreenscrapeSource.SIMPLE_FAILURE_DOCUMENT
        self.assert_(not source.login_was_successful(document))
    
    def test6(self):
        """Logging in will get response from connection"""
        source = LoginScreenscrapeSource()
        
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
    
