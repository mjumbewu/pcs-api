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
        source.login_to_pcs = lambda username, password: \
            ("<html><head><title>Please Login</title></head><body></body></html>", {})
        session = source.get_new_session('uid', 'pass')
        self.assert_(session is None)
    
    def test4(self):
        """Expected session is returned from a successful login."""
        source = LoginScreenscrapeSource()
        source.login_to_pcs = lambda username, password: \
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
    
