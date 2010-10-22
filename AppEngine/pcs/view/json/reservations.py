import datetime
import os

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from pcs.view import _ReservationsViewInterface
from util.abstract import override
from util.TimeZone import to_isostring

class ReservationsJsonView (_ReservationsViewInterface):
    @override
    def render_reservations(self, session, reservations, page_num, total_pages):
        reservations.sort(key=lambda res: res.start_time)
        
        data = {'reservation_list':{
            'page': page_num,
            'num_pages': total_pages,
            'reservations': []
        }}
        for reservation in reservations:
            res_data = {
                'id' : reservation.id,
                'start_time' : to_isostring(reservation.start_time),
                'end_time' : to_isostring(reservation.end_time),
                'vehicle' : {
                    'id' : reservation.vehicle.id,
                    'model' : {
                        'name' : reservation.vehicle.model.name
                    },
                    'pod' : {
                        'id' : reservation.vehicle.pod.id,
                        'name' : reservation.vehicle.pod.name
                    }
                }
            }
            data['reservation_list']['reservations'].append(res_data)
        
        # Sort the keys, so that tests are repeatable.
        return json.dumps(data, sort_keys=True, indent=2)
    
    @override
    def render_successful_new_reservation(self, session, reservation):
        values = {
            'session' : session,
            'reservation' : reservation
        }
        
        path = os.path.join(os.path.dirname(__file__), 'reservation-confirmation.html')
        response = self.render_method(path, values)
        return response

