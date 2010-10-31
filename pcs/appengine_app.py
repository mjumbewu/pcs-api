from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcs.wsgi_handlers.appengine.availability import LocationAvailabilityJsonHandler
from pcs.wsgi_handlers.appengine.locations    import LocationsJsonHandler
from pcs.wsgi_handlers.appengine.reservations import ReservationJsonHandler
from pcs.wsgi_handlers.appengine.reservations import ReservationsJsonHandler
from pcs.wsgi_handlers.appengine.session      import SessionJsonHandler

application = webapp.WSGIApplication(
        [('/session.json', SessionJsonHandler),
         ('/locations.json', LocationsJsonHandler),
         ('/locations/(.*)/availability.json', LocationAvailabilityJsonHandler),
         ('/reservation/(.*).json', ReservationJsonHandler),
         ('/reservations.json', ReservationsJsonHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
