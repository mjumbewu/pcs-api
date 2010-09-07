"""Package for the wsgi user input source."""

from google.appengine.ext import webapp

from util.TimeZone import Eastern

class WsgiParameterError (Exception):
    pass

class _SessionBasedHandler (webapp.RequestHandler):
    def __init__(self, session_source, error_view):
        super(_SessionBasedHandler, self).__init__()
        
        self.session_source = session_source
        self.error_view = error_view
    
    def get_user_id(self):
        user_id = self.request.cookies.get('suser', None)
        if user_id is None:
            raise WsgiParameterError('Could not find user id.')
        return user_id
    
    def get_session_id(self):
        session_id = self.request.cookies.get('sid', None)
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
        return self.error_view.get_error(None, type(error).__name__ + ': ' + str(error))

class _TimeRangeBasedHandler (webapp.RequestHandler):
    def __init__(self):
        super(_TimeRangeBasedHandler, self).__init__()
    
    def get_time_range(self):
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
        
        
