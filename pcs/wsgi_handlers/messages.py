import httplib
import urllib
import Cookie as cookielib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.session import Session

class MessagesHandler (webapp.RequestHandler):
    pass


application = webapp.WSGIApplication(
        [('/messages', MessagesHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
