import unittest
import StringIO

from util.testing import Stub

from pcs.input.wsgi.login import LoginHandler
from pcs.view import _LoginViewInterface
class LoginHandlerTest (unittest.TestCase):
    def testShouldRespondWithLoginForm(self):
        # Given...
        @Stub(_LoginViewInterface)
        class StubLoginView (object):
            def get_login_form(self, userid):
                return 'LoginForm'
        
        class StubRequest (dict):
            pass
        
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
        
        login_view = StubLoginView()
        handler = LoginHandler(login_view)
        handler.request = StubRequest()
        handler.response = StubResponse()
        
        # When...
        handler.get()
        
        # Then...
        response_body = handler.response.out.getvalue()
        self.assertEqual(response_body, 'LoginForm')

from pcs.input.wsgi.login import LoginHtmlHandler
from pcs.view.html.login import LoginHtmlView
class LoginHtmlHandlerTest (unittest.TestCase):
    def setUp(self):
        class StubRequest (dict):
            pass
        
        class StubResponse (object):
            out = StringIO.StringIO()
            def set_status(self, status):
                self.status = status
        
        self.request = StubRequest()
        self.response = StubResponse()
    
    def testShouldBeInitializedWithALoginHtmlView(self):
        handler = LoginHtmlHandler()
        
        self.assertEqual(handler.login_view.__class__.__name__, 'LoginHtmlView')
    
    def testShouldRespondWithAnEmptyLoginFormWhenNoUserIdIsProvided(self):
        handler = LoginHtmlHandler()
        handler.request = self.request
        handler.response = self.response

from pcs.view.html.login import LoginHtmlView
class LoginHtmlViewTest (unittest.TestCase):
    def testShouldReturnHtmlContentForSigningIn(self):
        """The HTML view returned should be a form for signing in."""
        
        # Given...
        view = LoginHtmlView()
        
        # When...
        response_body = view.get_login_form('myuser')
        
        # Then...
        expected_body = \
"""<!DOCTYPE html>

<html>
  <head>
    <title>Philly Car Share</title>
  </head>
  
  <body>
    <h1>Please Login</h1>
    <form action="/session.html" method="POST">
      <div>
        <label for="username">User ID:</label>
        <input type="text" value="myuser" name="username" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" name="password" />
      </div>
      <input type="submit" />
    </form>
  </body>
</html>

"""
        response_body = response_body.replace('<','&lt;')
        response_body = response_body.replace('>','&gt;')
        expected_body = expected_body.replace('<','&lt;')
        expected_body = expected_body.replace('>','&gt;')
        
        self.assertEqual(response_body, expected_body)


