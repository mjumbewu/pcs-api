import datetime
import httplib
import re
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib
import time

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from pcs.data.pod import Pod
from pcs.data.vehicle import PriceEstimate
from pcs.data.vehicle import VehicleType
from pcs.data.reservation import Reservation
from pcs.source import _ReservationsSourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from pcs.source.screenscrape.pcsconnection import PcsConnection
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup
from util.TimeZone import Eastern
from util.TimeZone import to_timestamp

class ReservationsScreenscrapeSource (_ReservationsSourceInterface):
    
    def __init__(self, host="reservations.phillycarshare.org",
                 upcoming_path="/my_reservations.php?mv_action=main",
                 past_path="/my_reservations.php?mv_action=main",
                 price_path="/ajax_estimate.php?slider=true"):
        super(ReservationsScreenscrapeSource, self).__init__()
        self.__host = host
        self.__upcoming_path = upcoming_path
        self.__past_path = past_path
        self.__price_path = price_path
    
    def get_driver_query(self, driverid):
        query = "main[multi_filter][driver_pk]=%s" % (driverid)
        return query
    
    def get_datefilter_query(self, year, month):
        query = "main[multi_filter][history][yearmonth]=%s%02d" % (year, month)
        return query
    
    def upcoming_reservations_from_pcs(self, conn, sessionid):
        host = self.__host
        path = self.__upcoming_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        query = ''
#        query = self.get_driver_query(driverid)
        connector = ''
#        connector = '&' if '?' in path else '?'
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "GET", {}, headers)
        return (response.read(), response.getheaders())
    
    def past_reservations_from_pcs(self, conn, sessionid, year, month):
        host = self.__host
        path = self.__past_path
        
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        query = ''
#        query = self.get_driver_query(driverid)
        query += self.get_datefilter_query(year, month)
#        query += '&' + self.get_datefilter_query(year, month)
        connector = '&' if '?' in path else '?'
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        
        response = conn.request(url, "GET", {}, headers)
        return (response.read(), response.getheaders())
    
    def get_html_data(self, response_body):
        html_data = BeautifulSoup(response_body)
        return html_data
    
    def get_text_from_td_data(self, td):
        td_text = td.text
        return td_text
    
    def get_pod_and_vehicle_from_td_data(self, td):
        pod_a = td.find('a')
        
        pod_url = pod_a['href']
        pod_names = pod_a.text
        
        url_match = re.match(r'my_fleet\.php\?mv_action=show&_r=\d+&pk=(?P<pod_id>\d+)', pod_url)
        podid = url_match.group('pod_id')
        
        names_match = re.match(r'(?P<pod_name>.*) - (?P<vehicle_model>.*)', pod_names)
        pod_name = names_match.group('pod_name')
        vehicle_model = names_match.group('vehicle_model')
        
        pod = Pod(podid)
        pod.url = pod_url
        pod.name = pod_name
        
        vehicle = VehicleType(None)
        vehicle.model = vehicle_model
        
        return pod, vehicle
    
    def get_time_from_td_data(self, td):
        time_pattern = r'(?P<hour>\d+):(?P<minute>\d+) (?P<midi>[ap])m [A-Za-z]+, (?P<month>[A-Za-z]+) (?P<day>\d+), (?P<year>\d+)'
        
        time_text = td.text
        time_match = re.match(time_pattern, time_text)
        
        months = { 'January':1, 'February':2, 'March':3, 'April':4, 
                       'May':5, 'June':6, 'July':7, 'August':8, 'September':9,
                       'October':10, 'November':11, 'December':12 }
        
        hour = int(time_match.group('hour'))
        if hour == 12:
            hour = 0
        minute = int(time_match.group('minute'))
        midi = time_match.group('midi')
        if midi == 'p':
            hour += 12
        month = months[time_match.group('month')]
        day = int(time_match.group('day'))
        year = int(time_match.group('year'))
        
        return datetime.datetime(year, month, day, hour, minute, tzinfo=Eastern)
    
    def get_price_from_td_data(self, td):
        price_a = td.find('a')
        
        price_pattern = r'\$(?P<dollars>[0-9.]+)'
        price_string = price_a.text
        
        price_match = re.match(price_pattern, price_string)
        price = PriceEstimate()
        price.total_amount = float(price_match.group('dollars'))
        
        return price
    
    def get_reservation_from_table_row_data(self, reservation_tr):
        tds = reservation_tr.findAll('td')
        
        reservation = None
        
        td_count = 0
        for td in tds:
            if td_count == 0:
                reservationid = \
                    self.get_text_from_td_data(td)
                reservation = Reservation(reservationid)
                
            elif td_count == 1:
                reservation.pod, reservation.vehicle = \
                    self.get_pod_and_vehicle_from_td_data(td)
                    
            elif td_count == 2:
                reservation.start_time = \
                    self.get_time_from_td_data(td)
                    
            elif td_count == 3:
                reservation.end_time = \
                    self.get_time_from_td_data(td)
                    
            elif td_count == 4:
                reservation.price = \
                    self.get_price_from_td_data(td)
                    
#            elif td_count == 5:
#                reservation.status = \
#                    self.get_text_from_td_data(td)
                    
            elif td_count == 6:
                reservation.memo = \
                    self.get_text_from_td_data(td)
            
            td_count += 1
        
        return reservation
    
    def get_pcs_connection(self):
        return PcsConnection()
    
    def get_reservation_data_from_html_data(self, html_data):
        reservations = []

        res_table = html_data.find('table', {'id': 'main_dlist_'})
        
        if res_table is not None:
            res_tbody = res_table.find('tbody')
            res_trs = res_tbody.findAll('tr')
            
            for res_tr in res_trs:
                reservation = self.get_reservation_from_table_row_data(res_tr)
                reservations.append(reservation)
        
        return reservations
    
    @override
    def get_reservations(self, sessionid, year_month=None):
        conn = self.get_pcs_connection()
        
        if year_month is None:
            pcs_body, pcs_head = \
                self.upcoming_reservations_from_pcs(conn, sessionid)
        else:
            pcs_body, pcs_head = \
                self.past_reservations_from_pcs(conn, sessionid, *year_month)
        
        reservations_html_doc = self.get_html_data(pcs_body)
        reservations = self.get_reservation_data_from_html_data(reservations_html_doc)
        
        return reservations

