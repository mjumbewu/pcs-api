"""Package for the wsgi user input source."""
import re
import sys

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from util.TimeZone import Eastern
from util.TimeZone import from_isostring
from util.TimeZone import from_timestamp

class WsgiParameterError (Exception):
    pass

class _SessionBasedHandler (object):
    def __init__(self, session_source, error_view):
        super(_SessionBasedHandler, self).__init__()
        
        self.session_source = session_source
        self.error_view = error_view
    
    def get_session_data(self):
        session_string = self.request.cookies.get('session', None)
        if session_string is None:
            raise WsgiParameterError('Cound not find session cookie')
        
        session_string = session_string.replace(r'\"',r'"')[1:-1]
        try:
            return json.loads(session_string)
        except ValueError:
            raise Exception(repr(session_string))
    
    def get_user_id(self):
        session_data = self.get_session_data()
        user_id = session_data.get('user', None)
        if user_id is None:
            raise WsgiParameterError('Could not find user id.')
        return user_id
    
    def get_session_id(self):
        session_data = self.get_session_data()
        session_id = session_data.get('id', None)
        if session_id is None:
            raise WsgiParameterError('Could not find session id.')
        return session_id
    
    def get_session(self, userid, sessionid):
        """
        Attempt to get a session using username and password credentials. If no
        password is available, attempt to find an existing session id to use.
        @return: A valid session or None
        """
        session = self.session_source.fetch_session(userid, sessionid)
        return session

    def generate_error(self, error):
        import traceback
        
        _,_,tb = sys.exc_info()
        tb_str = '\n'.join(traceback.format_tb(tb))
        return self.error_view.render_error(None, type(error).__name__ + ': ' + str(error), tb_str)

class _TimeRangeBasedHandler (object):
    def __init__(self):
        super(_TimeRangeBasedHandler, self).__init__()
    
    def get_time_range(self):
        return self.get_single_iso_datetime_range()
    
    def get_epoch_time_range(self):
        import datetime
        start_time_str = self.request.get('start_time')
        end_time_str = self.request.get('end_time')
        
        now_time = datetime.datetime.now(Eastern) + datetime.timedelta(minutes=1)
        if start_time_str:
            start_time = from_timestamp(start_time_str)
        else:
            start_time = now_time
        
        if end_time_str:
            end_time = from_timestamp(end_time_str)
        else:
            end_time = now_time + datetime.timedelta(hours=3)
        
        return start_time, end_time
    
    def get_separate_iso_date_and_time_range(self):
        """
        A custom redefinition of get_time_range, as we expect the results from
        HTML date and time form fields for the start and end times.  The normal
        method operates on UTC timestamps.
        """
        import datetime
        start_date_str = self.request.get('start_date')
        end_date_str = self.request.get('end_date')
        start_time_str = self.request.get('start_time')
        end_time_str = self.request.get('end_time')
        
        now_time = datetime.datetime.now(Eastern) + datetime.timedelta(minutes=1)
        if start_date_str and start_time_str:
            start_dt_str = "%sT%s" % (start_date_str, start_time_str)
            start_time = from_isostring(start_dt_str)
        else:
            start_time = now_time
        
        if end_date_str and end_time_str:
            end_dt_str = "%sT%s" % (end_date_str, end_time_str)
            end_time = from_isostring(end_dt_str)
        else:
            end_time = now_time + datetime.timedelta(hours=3)
        
        return start_time, end_time
        
    def get_single_iso_datetime_range(self):
        """
        A custom redefinition of get_time_range.  This method operates on start
        and end dates and times specified as single ISO8601 datetime strings.
        """
        import datetime
        start_time_str = self.request.get('start_time')
        end_time_str = self.request.get('end_time')
        
        now_time = datetime.datetime.now(Eastern) + datetime.timedelta(minutes=1)
        if start_time_str:
            start_time = from_isostring(start_time_str)
        else:
            start_time = now_time
        
        if end_time_str:
            end_time = from_isostring(end_time_str)
        else:
            end_time = now_time + datetime.timedelta(hours=3)
        
        return start_time, end_time
        
        
