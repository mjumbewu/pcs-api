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
from pcs.data.vehicle import Vehicle
from pcs.data.vehicle import VehicleModel
from pcs.data.vehicle import AvailableVehicle
from pcs.fetchers import _AvailabilitySourceInterface
from pcs.fetchers.screenscrape import ScreenscrapeParseError
from pcs.fetchers.screenscrape.pcsconnection import PcsConnection
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup
from util.TimeZone import Eastern
from util.TimeZone import to_timestamp

class AvailabilityScreenscrapeSource (_AvailabilitySourceInterface):
    """
    Responsible for logging in and constructing a session from a screenscrape
    of a PhillyCarShare response.
    """
    SIMPLE_FAILURE_DOCUMENT = "<html><head><title>Please Login</title></head><body></body></html>"
    
    def __init__(self, host="reservations.phillycarshare.org",
                 vehicles_path="/results.php?reservation_id=0&flexible=on&show_everything=on&offset=0",
                 vehicle_path="/lightbox.php",
                 price_path="/ajax_estimate.php?slider=true"):
        super(AvailabilityScreenscrapeSource, self).__init__()
        self.__host = host
        self.__vehicles_path = vehicles_path
        self.__vehicle_path = vehicle_path
        self.__price_path = price_path
        
        self._vehicle_cache = {}
    
    def get_location_query(self, locationid):
        if isinstance(locationid, (basestring, int)):
            query = 'location=driver_locations_%s' % locationid
            return query
        
        if isinstance(locationid, (list, tuple)) and len(locationid) == 2:
            latitude = locationid[0]
            longitude = locationid[1]
            # Note: The initial empty 'location=' parameter must be there, or 
            #       PCS will just use the default location profile.  Not fun
            #       figuring that one out.
            query = 'location=&location_latitude=%s&location_longitude=%s' % \
                (latitude, longitude)
            return query
        
        raise Exception('unrecognizable location: %r' % locationid)
    
    def get_time_query(self, start_time, end_time):
        syear = start_time.year
        smonth = start_time.month
        sday = start_time.day
        shour = start_time.hour
        sminute = start_time.minute
        stime = sminute*60 + shour*3600
        
        eyear = end_time.year
        emonth = end_time.month
        eday = end_time.day
        ehour = end_time.hour
        eminute = end_time.minute
        etime = eminute*60 + ehour*3600
        
        query = r"start_date=%s/%s/%s&start_time=%s&end_date=%s/%s/%s&end_time=%s" % \
            (smonth, sday, syear, stime, emonth, eday, eyear, etime)
        return query
    
    def availability_from_pcs(self, conn, sessionid, locationid, start_time, end_time):
        """
        Attempts to load a session from the connection with the given session
        id.
        
        @return: The server response.  If reconnection failed, the response
          body should be identifiable as an invalid session.
        """
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        query = self.get_location_query(locationid)
        query += '&' + self.get_time_query(start_time, end_time)
        connector = '&' if '?' in self.__vehicles_path else '?'
        
        url = "http://%s%s%s%s" % (self.__host, self.__vehicles_path, connector, query)
        
        response = conn.request(url, "GET", {}, headers)
        return (response.read(), response.getheaders())
    
    def get_json_data(self, response_body):
        """
        Load json data from the given string, which should be the response
        from results.php
        """
        json_data = json.loads(response_body)
        return json_data
    
    def get_html_data(self, json_data):
        """
        Load HTML data from the given json data, which is a json documents
        representation of the reponse from results.php
        """
        try:
            pod_divs = json_data['pods']
        except KeyError:
            # json_data['status'] == 1 ==> start time is in the past.
            raise ScreenscrapeParseError('Json data has no "pods" key: %r' % json_data)
        html_body = '<html><body>%s</body></html>' % (''.join(pod_divs))
        html_data = BeautifulSoup(html_body)
        return html_data
    
    def get_pod_and_distance_from_html_data(self, pod_info_div):
        pod_link = pod_info_div.find('a')
        
        matches = re.match(r'(?P<name>.*) - (?P<dist>[0-9]+\.?[0-9]*) mile\(s\)',
                           pod_link.text)
        pod_name = str(matches.group('name'))
        pod_dist = float(matches.group('dist'))
        
        matches = re.match(r'MV\.controls\.results\.show_pod_details\((?P<pod_id>[0-9]+)\)',
                          pod_link['onclick'])
        pod_id = matches.group('pod_id')
        
        pod = Pod(pod_id)
        pod.name = pod_name
        return pod, pod_dist
    
    def assign_vehicle_availability_stipulation(self, vehicle, stipulation):
        from_pattern = r'Available from (?P<hour>[0-9]+):(?P<minute>[0-9]+) (?P<midi>[ap])m on (?P<month>[0-9]+)/(?P<day>[0-9]+)$'
        until_pattern = r'Available until (?P<hour>[0-9]+):(?P<minute>[0-9]+) (?P<midi>[ap])m on (?P<month>[0-9]+)/(?P<day>[0-9]+)$'
        between_pattern = r'Available from (?P<hour1>[0-9]+):(?P<minute1>[0-9]+) (?P<midi1>[ap])m on (?P<month1>[0-9]+)/(?P<day1>[0-9]+) to (?P<hour2>[0-9]+):(?P<minute2>[0-9]+) (?P<midi2>[ap])m on (?P<month2>[0-9]+)/(?P<day2>[0-9]+)$'
        
        from_match = re.match(from_pattern, stipulation)
        if from_match is not None:
            hour = int(from_match.group('hour'))
            if hour == 12:
                hour = 0
            minute = int(from_match.group('minute'))
            midi = from_match.group('midi')
            if midi == 'p':
                hour += 12
            month = int(from_match.group('month'))
            day = int(from_match.group('day'))
            
            now = datetime.datetime.now(Eastern)
            
            available_from = datetime.datetime(now.year, month, day, hour, minute, tzinfo=Eastern)
            if available_from < now:
                available_from = available_from.replace(year=now.year+1)
            
            vehicle.earliest = available_from
            return
        
        until_match = re.match(until_pattern, stipulation)
        if until_match is not None:
            hour = int(until_match.group('hour'))
            minute = int(until_match.group('minute'))
            midi = until_match.group('midi')
            if midi == 'p':
                hour += 12
            month = int(until_match.group('month'))
            day = int(until_match.group('day'))
            
            now = datetime.datetime.now(Eastern)
            
            available_until = datetime.datetime(now.year, month, day, hour, minute, tzinfo=Eastern)
            if available_until < now:
                available_until = available_until.replace(year=now.year+1)
            
            vehicle.latest = available_until
            return
        
        between_match = re.match(between_pattern, stipulation)
        if between_match is not None:
            # from...
            hour = int(between_match.group('hour1'))
            minute = int(between_match.group('minute1'))
            midi = between_match.group('midi1')
            if midi == 'p':
                hour += 12
            month = int(between_match.group('month1'))
            day = int(between_match.group('day1'))
            
            now = datetime.datetime.now(Eastern)
            
            available_from = datetime.datetime(now.year, month, day, hour, minute, tzinfo=Eastern)
            if available_from < now:
                available_from = available_from.replace(year=now.year+1)
            
            # until...
            hour = int(between_match.group('hour2'))
            minute = int(between_match.group('minute2'))
            midi = between_match.group('midi2')
            if midi == 'p':
                hour += 12
            month = int(between_match.group('month2'))
            day = int(between_match.group('day2'))
            
            available_until = datetime.datetime(available_from.year, month, day, hour, minute, tzinfo=Eastern)
            if available_until < available_from:
                available_until = available_until.replace(year=available_from.year+1)
            
            vehicle.earliest = available_from
            vehicle.latest = available_until
            return
        
    
    def get_vehicle_from_html_data(self, pod, vehicle_info_div, start_time, end_time):
        vehicle_header = vehicle_info_div.find('h4')
        vehicle_name = vehicle_header.text
        
        availability_div = vehicle_info_div.find('div', {'class':'timestamp'})
        availability_p = availability_div.find('p')
        
        reserve_div = vehicle_info_div.find('div', {'class':'reserve'})
        reserve_a = reserve_div.find('a')
        lightbox_script = reserve_a['href']
        
        match = re.match(r"javascript:MV.controls.reserve.lightbox.create\('(?P<start_time>[0-9]*)', '(?P<end_time>[0-9]*)', '(?P<vehicle_id>[0-9]*)', ''\);", lightbox_script)
        vehicleid = match.group('vehicle_id')
        
        model = VehicleModel()
        model.name = vehicle_name
        
        vehicle = Vehicle(vehicleid)
        vehicle.model = model
        vehicle.pod = pod
        
        vehicle_availability = AvailableVehicle()
        vehicle_availability.vehicle = vehicle
        vehicle_availability.start_time = start_time
        vehicle_availability.end_time = end_time
        
        # Since the availability information is in the div too, store it.
        if availability_p['class'] == 'good':
            vehicle_availability.availability = 'full'
            vehicle_availability.score = 1
        elif availability_p['class'] == 'bad':
            vehicle_availability.availability = 'none'
            vehicle_availability.score = 0
        elif availability_p['class'] == 'maybe':
            vehicle_availability.availability = 'part'
            vehicle_availability.score = 0.5
            self.assign_vehicle_availability_stipulation(vehicle_availability, availability_p.text)
        
        return vehicle_availability
    
    def create_vehicles_from_pcs_availability_doc(self, pcs_results_doc, start_time, end_time):
        vehicle_availabilities = []
        current_pod = None
        current_dist = None
        
        body = pcs_results_doc.find('body')
        info_divs = body.findAll('div', recursive=False)
        for info_div in info_divs:
            if 'pod_top' in info_div['class']:
                pod_div = info_div
                current_pod, current_dist = self.get_pod_and_distance_from_html_data(pod_div)
            elif 'pod_bot' in info_div['class']:
                vehicle_div = info_div
                vehicle_availability = self.get_vehicle_from_html_data(current_pod, vehicle_div, start_time, end_time)
                vehicle_availabilities.append(vehicle_availability)
        
        return vehicle_availabilities
    
    def create_host_connection(self):
        return PcsConnection()
    
    @override
    def fetch_available_vehicles_near(self, sessionid, locationid, start_time, end_time):
        conn = self.create_host_connection()
        
        pcs_available_body, pcs_available_headers = \
            self.availability_from_pcs(conn, sessionid, locationid, start_time, end_time)
        self._body = pcs_available_body
        self._headers = pcs_available_headers
        
        json_availability_data = self.get_json_data(pcs_available_body)
        html_pods_data = self.get_html_data(json_availability_data)
        
        vehicles = self.create_vehicles_from_pcs_availability_doc(html_pods_data, start_time, end_time)
        return vehicles
    
    def vehicle_info_from_pcs(self, conn, sessionid, vehicleid, start_time, end_time):
        if (sessionid, vehicleid, start_time, end_time) not in self._vehicle_cache:
            host = self.__host
            path = self.__vehicle_path
            # The PhillyCarShare servers do not take into account time zone 
            # information in their timestamp calculations, so we have to reverse
            # our timezone info.  However, we have to keep it in the first place
            # because Google's servers aren't necessarily on Eastern time (but 
            # PhillyCarShare always will be).
            start_stamp = to_timestamp(start_time)
            end_stamp = to_timestamp(end_time)
            
            url = 'http://%s%s' % (host, path)
            method = 'POST'
            data = urllib.urlencode({'mv_action':'add',
                    'default[stack_pk]':vehicleid,
                    'default[start_stamp]':str(int(start_stamp)),
                    'default[end_stamp]':str(int(end_stamp))})
            headers = { 'Cookie':'sid=%s' % sessionid }
            response = \
                conn.request(url, method, data, headers)
            
            self._vehicle_cache[(sessionid, vehicleid, start_time, end_time)] = (response.read(), response.getheaders())
        return self._vehicle_cache[(sessionid, vehicleid, start_time, end_time)]
    
    def get_html_vehicle_data(self, html_body):
        html_data = BeautifulSoup('<html><body>%s</body></html>' % html_body)
        return html_data
    
    def create_vehicle_from_pcs_information_doc(self, html_data):
        vehicleid_tag = html_data.find('input', {'type':'hidden', 'name':'add[stack_pk]'})
        if vehicleid_tag is None:
            raise ScreenscrapeParseError('Vehicle ID not found in vehicle information.')
        
        vehicleid = vehicleid_tag['value']
        
        model_tag = html_data.find('span', {'id':'add_stack_pk_vt'})
        if model_tag is None:
            raise ScreenscrapeParseError('Vehicle model not found in vehicle information.')
        
        model_name = model_tag.text
        
        model = VehicleModel()
        model.name = model_name
        
        vehicle = Vehicle(vehicleid)
        vehicle.model = model
        return vehicle
    
    @override
    def fetch_vehicle(self, sessionid, vehicleid, start_time, end_time):
        conn = self.create_host_connection()
        
        pcs_vehicle_body, pcs_vehicle_headers = \
            self.vehicle_info_from_pcs(conn, sessionid, vehicleid, start_time, end_time)
        html_vehicle_data = self.get_html_vehicle_data(pcs_vehicle_body)
        
        vehicle = self.create_vehicle_from_pcs_information_doc(html_vehicle_data)
        return vehicle
    
    def transaction_from_pcs_information_doc(self, html_data):
        tid_field = html_data.find('input', {'id':'add_tid_'})
        return tid_field['value']
    
    @override
    def fetch_updated_transaction(self, sessionid, vehicleid, start_time, end_time):
        conn = self.create_host_connection()
        
        pcs_vehicle_body, pcs_vehicle_headers = \
            self.vehicle_info_from_pcs(conn, sessionid, vehicleid, start_time, end_time)
        html_vehicle_data = self.get_html_vehicle_data(pcs_vehicle_body)
        
        transactionid = self.transaction_from_pcs_information_doc(html_vehicle_data)
        return transactionid
    
    def vehicle_price_estimate_from_pcs(self, conn, sessionid, vehicleid, start_time, end_time):
        host = self.__host
        path = self.__price_path
        connector = '&' if '?' in path else '?'

        start_stamp = to_timestamp(start_time)
        end_stamp = to_timestamp(end_time)
        
        query = 'mv_action=add&stack_pk=%s&start_stamp=%s&end_stamp=%s' % \
            (vehicleid, start_stamp, end_stamp)
        
        url = "http://%s%s%s%s" % (host, path, connector, query)
        method = 'GET'
        data = {}
        headers = {'Cookie': 'sid=%s' % sessionid}
        response = \
            conn.request(url, method, data, headers)
        
        return response.read(), response.getheaders()
    
    def create_price_from_pcs_price_estimate_doc(self, json_price_obj):
        price = PriceEstimate()
        price.available_balance = json_price_obj['available_balance'][0]
        price.available_credit = json_price_obj['available_credit'][0]
        price.applied_credit = json_price_obj['applied_credit'][0]
        price.distance = json_price_obj['distance'][0]
        price.hourly_rate = json_price_obj['hourly_rate'][0]
        price.daily_rate = json_price_obj['daily_rate'][0]
        price.time_amount = json_price_obj['time_amount'][0]
        price.distance_amount = json_price_obj['distance_amount'][0]
        price.tax_amount = json_price_obj['tax_amount'][0]
        price.fee_amount = json_price_obj['fee_amount'][0]
        price.total_amount = json_price_obj['total_amount'][0]
        price.amount_due = json_price_obj['amount_due'][0]
        
        return price
    
    @override
    def fetch_vehicle_price_estimate(self, sessionid, vehicleid, start_time, end_time):
        conn = self.create_host_connection()
        
        pcs_price_body, pcs_price_headers = \
            self.vehicle_price_estimate_from_pcs(conn, sessionid, vehicleid, start_time, end_time)
        json_price_data = self.get_json_data(pcs_price_body)
        
        price = self.create_price_from_pcs_price_estimate_doc(json_price_data)
        return price
