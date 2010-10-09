"""Package for the wsgi user input source."""
import re
import sys

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from google.appengine.ext import webapp

from util.TimeZone import Eastern

class WsgiParameterError (Exception):
    pass

class _SessionBasedHandler (webapp.RequestHandler):
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
        session = self.session_source.get_existing_session(userid, sessionid)
        return session

    def generate_error(self, error):
        import traceback
        
        _,_,tb = sys.exc_info()
        tb_str = traceback.format_tb(tb)
        return self.error_view.render_error(None, type(error).__name__ + ': ' + str(error) + '\n'.join(tb_str))

class _TimeRangeBasedHandler (webapp.RequestHandler):
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
            start_time = datetime.datetime.fromtimestamp(int(start_time_str), Eastern)
        else:
            start_time = now_time
        
        if end_time_str:
            end_time = datetime.datetime.fromtimestamp(int(end_time_str), Eastern)
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
            date_match = re.match('(?P<year>[0-9]+)-(?P<month>[0-9]+)-(?P<day>[0-9]+)', start_date_str)
            time_match = re.match('(?P<hour>[0-9]+):(?P<minute>[0-9]+)', start_time_str)
            start_time = datetime.datetime(int(date_match.group('year')),
                int(date_match.group('month')),
                int(date_match.group('day')),
                int(time_match.group('hour')),
                int(time_match.group('minute')), tzinfo=Eastern)
        else:
            start_time = now_time
        
        if end_date_str and end_time_str:
            date_match = re.match('(?P<year>[0-9]+)-(?P<month>[0-9]+)-(?P<day>[0-9]+)', end_date_str)
            time_match = re.match('(?P<hour>[0-9]+):(?P<minute>[0-9]+)', end_time_str)
            end_time = datetime.datetime(int(date_match.group('year')),
                int(date_match.group('month')),
                int(date_match.group('day')),
                int(time_match.group('hour')),
                int(time_match.group('minute')), tzinfo=Eastern)
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
            time_match = re.match('(?P<year>[0-9]+)-(?P<month>[0-9]+)-(?P<day>[0-9]+)T(?P<hour>[0-9]+):(?P<minute>[0-9]+)', start_time_str)
            start_time = datetime.datetime(int(time_match.group('year')),
                int(time_match.group('month')),
                int(time_match.group('day')),
                int(time_match.group('hour')),
                int(time_match.group('minute')), tzinfo=Eastern)
        else:
            start_time = now_time
        
        if end_time_str:
            time_match = re.match('(?P<year>[0-9]+)-(?P<month>[0-9]+)-(?P<day>[0-9]+)T(?P<hour>[0-9]+):(?P<minute>[0-9]+)', end_time_str)
            end_time = datetime.datetime(int(time_match.group('year')),
                int(time_match.group('month')),
                int(time_match.group('day')),
                int(time_match.group('hour')),
                int(time_match.group('minute')), tzinfo=Eastern)
        else:
            end_time = now_time + datetime.timedelta(hours=3)
        
        return start_time, end_time
        
        
