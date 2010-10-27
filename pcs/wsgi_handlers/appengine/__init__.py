"""Package for the appengine wsgi handlers."""
from google.appengine.ext import webapp

class _AppEngineBasedHandler (webapp.RequestHandler):
    def __init__(self):
        super(_AppEngineBasedHandler, self).__init__()

