import os
from google.appengine.ext.webapp import template

class LoginHtmlView (object):
    @staticmethod
    def get_login_form(username=''):
        values = {
            'username': username
        }
        
        path = os.path.join(os.path.dirname(__file__), 'login.html')
        response = template.render(path, values)
        return response
    
