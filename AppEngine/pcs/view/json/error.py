import os
from google.appengine.ext.webapp import template

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from pcs.view import _ErrorViewInterface
from util.abstract import override

class ErrorJsonView (_ErrorViewInterface):
    @override
    def render_error(self, error_code, error_msg, error_detail):
        """
        Return an error response.
        """
        data = {
            'error' : {
                'code' : error_code,
                'msg' : error_msg,
                'detail' : error_detail
            }
        }
        
        return json.dumps(data);

