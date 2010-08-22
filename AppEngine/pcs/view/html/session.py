import os
from google.appengine.ext.webapp import template

from pcs.view import _SessionViewInterface
from util.abstract import override

class SessionHtmlView (_SessionViewInterface):
    @override
    def get_session_overview(self, session):
        """
        Return a response with overview information about the given session.
        """
        values = {
            'session': session
        }
        
        path = os.path.join(os.path.dirname(__file__), 'session_home.html')
        response = template.render(path, values)
        return response
    
