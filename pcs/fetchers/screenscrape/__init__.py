"""Package for screenscraping as a data source."""

class ErrorWithCode (Exception):
    def __init__(self, msg=None, code=None):
        super(ErrorWithCode, self).__init__(msg)
        self.code = code

class ScreenscrapeParseError (ErrorWithCode):
    pass

class ScreenscrapeFetchError (ErrorWithCode):
    pass
