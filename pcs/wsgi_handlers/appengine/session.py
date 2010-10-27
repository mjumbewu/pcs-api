from pcs.wsgi_handlers.appengine import _AppEngineBasedHandler

from pcs.wsgi_handlers.session import SessionHandler
from pcs.wsgi_handlers.session import SessionHtmlHandler
from pcs.wsgi_handlers.session import SessionJsonHandler as _BaseSessionJsonHandler

class SessionJsonHandler (_BaseSessionJsonHandler, _AppEngineBasedHandler):
    pass
