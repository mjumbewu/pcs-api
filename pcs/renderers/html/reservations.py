import datetime
import os

from google.appengine.ext.webapp import template

from pcs.renderers import _ReservationsViewInterface
from util.abstract import override
from util.TimeZone import to_xchange_time

class ReservationsHtmlView (_ReservationsViewInterface):
    def __init__(self, render_method=template.render):
        self.render_method = render_method
    
    @override
    def get_reservations(self, session, reservations):
        reservations.sort(key=lambda res: res.start_time)
        reservations.reverse()
        reservations.sort(key=lambda res: res.status)
        
        for reservation in reservations:
            reservation.start_stamp = to_xchange_time(reservation.start_time)
            reservation.end_stamp = to_xchange_time(reservation.end_time)
        
        values = {
            'session': session,
            'reservations': reservations,
        }
        
        path = os.path.join(os.path.dirname(__file__), 'reservations.html')
        response = self.render_method(path, values)
        return response
    
    @override
    def get_successful_new_reservation(self, session, reservation):
        values = {
            'session' : session,
            'reservation' : reservation
        }
        
        path = os.path.join(os.path.dirname(__file__), 'reservation-confirmation.html')
        response = self.render_method(path, values)
        return response

