import os
from google.appengine.ext.webapp import template

class SessionHtmlView (object):
    @staticmethod
    def get_session_overview(session):
        """
        Return a response with overview information about the given session.
        """
        values = {
            'session': session
        }
        
        path = os.path.join(os.path.dirname(__file__), 'session_home.html')
        response = template.render(path, values)
        return response
    
