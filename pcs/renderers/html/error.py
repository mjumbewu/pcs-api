import os
from google.appengine.ext.webapp import template

from pcs.renderers import _ErrorViewInterface
from util.abstract import override

class ErrorHtmlView (_ErrorViewInterface):
    @override
    def get_error(self, error_code, error_msg, error_detail):
        """
        Return a response with overview information about the given session.
        """
        values = {
            'error_code': error_code,
            'error_msg': error_msg
        }
        
        path = os.path.join(os.path.dirname(__file__), 'session_error.html')
        response = template.render(path, values)
        return response
    
