import os
from google.appengine.ext.webapp import template

from pcs.view import _ErrorViewInterface
from util.abstract import override

class ErrorJsonView (_ErrorViewInterface):
    @override
    def get_error(self, error_code, error_msg):
        """
        Return an error response.
        """
        values = {
            'error_code': error_code,
            'error_msg': error_msg
        }
        
        path = os.path.join(os.path.dirname(__file__), 'error.json')
        response = template.render(path, values)
        return response
    
