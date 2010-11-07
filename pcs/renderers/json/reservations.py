import datetime
import os

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from pcs.renderers import _ReservationsViewInterface
from util.abstract import override
from util.TimeZone import to_isostring

class ReservationsJsonView (_ReservationsViewInterface):
    def format_res_data(self, reservation):
        res_data = {
            'start_time' : to_isostring(reservation.start_time),
            'end_time' : to_isostring(reservation.end_time),
            'vehicle' : {
                'id' : reservation.vehicle.id,
            }
        }
        
        if hasattr(reservation, 'liveid'):
            res_data['liveid'] = reservation.liveid
        if hasattr(reservation, 'logid'):
            res_data['logid'] = reservation.logid
        if hasattr(reservation.vehicle, 'model'):
            res_data['vehicle']['model'] = {
                    'name' : reservation.vehicle.model.name
                }
        if hasattr(reservation.vehicle, 'pod'):
            res_data['vehicle']['pod'] = {
                    'id' : reservation.vehicle.pod.id,
                    'name' : reservation.vehicle.pod.name
                }
        if hasattr(reservation, 'price'):
            res_data['price'] = {
                    'total_amount' : reservation.price.total_amount
                }
        
        return res_data
    
    @override
    def render_reservations(self, session, reservations, page_num, total_pages):
        reservations.sort(key=lambda res: res.start_time)
        
        data = {'reservation_list':{
            'page': page_num,
            'num_pages': total_pages,
            'reservations': []
        }}
        for reservation in reservations:
            res_data = self.format_res_data(reservation)
            data['reservation_list']['reservations'].append(res_data)
        
        # Sort the keys, so that tests are repeatable.
        return json.dumps(data, sort_keys=True, indent=2)
    
    @override
    def render_confirmation(self, session, reservation, event):
        data = {'confirmation':{
            'reservation' : self.format_res_data(reservation),
            'event' : event
        }}
        
        return json.dumps(data, sort_keys=True, indent=2)
    
    @override
    def render_reservation(self, session, reservation):
        data = {'reservation':self.format_res_data(reservation)}
        return json.dumps(data, sort_keys=True, indent=2)


