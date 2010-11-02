"""Package for screenscraping as a data source."""

class ErrorWithCode (Exception):
    def __init__(self, msg=None, code=None):
        super(ErrorWithCode, self).__init__(msg)
        self.code = code

class ScreenscrapeParseError (ErrorWithCode):
    pass

class ScreenscrapeFetchError (ErrorWithCode):
    pass

class _ScreenscrapeBase (object):
    def verify_pcs_response(self, response_body, response_headers=None):
        if 'Please&nbsp;sign&nbsp;in&nbsp;below:' in response_body:
            raise ScreenscrapeFetchError(
                'Your session is invalid.', 'invalid_session')
        
        return True
