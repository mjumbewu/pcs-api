import os
from google.appengine.ext.webapp import template

from pcs.renderers import _LoginViewInterface
from util.abstract import override

class LoginHtmlView (_LoginViewInterface):
    @override
    def get_login_form(self, userid=''):
        """
        Return a response with a mechanism for logging in.  For HTML, this is
        a login form.
        """
        values = {
            'username': userid
        }
        
        path = os.path.join(os.path.dirname(__file__), 'login.html')
        response = template.render(path, values)
        return response
    
