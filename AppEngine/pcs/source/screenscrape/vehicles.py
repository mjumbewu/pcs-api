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
from pcs.data.vehicle import Vehicle
from pcs.source import _VehiclesSourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from pcs.source.screenscrape.pcsconnection import PcsConnection
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup
from util.TimeZone import Eastern

class VehiclesScreenscrapeSource (_VehiclesSourceInterface):
    """
    Responsible for logging in and constructing a session from a screenscrape
    of a PhillyCarShare response.
    """
    SIMPLE_FAILURE_DOCUMENT = "<html><head><title>Please Login</title></head><body></body></html>"
    
    def __init__(self, host="reservations.phillycarshare.org",
                 vehicles_path="/results.php?reservation_id=0&flexible=on&show_everything=on&offset=0",
                 vehicle_path="/lightbox.php"):
        super(VehiclesScreenscrapeSource, self).__init__()
        self.__host = host
        self.__vehicles_path = vehicles_path
        self.__vehicle_path = vehicle_path
    
    def get_location_query(self, locationid):
        if isinstance(locationid, (basestring, int)):
            query = 'location=driver_locations_%s' % locationid
            return query
        
        if isinstance(locationid, (list, tuple)) and len(locationid) == 2:
            latitude = locationid[0]
            longitude = locationid[1]
            query = 'location_latitude=%s&location_longitude=%s' % \
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
        
        pod = Pod(pod_name)
        return pod, pod_dist
    
    def assign_vehicle_availability_stipulation(self, vehicle, stipulation):
        from_pattern = r'Available from (?P<hour>[0-9]+):(?P<minute>[0-9]+) (?P<midi>[ap])m on (?P<month>[0-9]+)/(?P<day>[0-9]+)$'
        until_pattern = r'Available until (?P<hour>[0-9]+):(?P<minute>[0-9]+) (?P<midi>[ap])m on (?P<month>[0-9]+)/(?P<day>[0-9]+)$'
        between_pattern = r'Available from (?P<hour1>[0-9]+):(?P<minute1>[0-9]+) (?P<midi1>[ap])m on (?P<month1>[0-9]+)/(?P<day1>[0-9]+) to (?P<hour2>[0-9]+):(?P<minute2>[0-9]+) (?P<midi2>[ap])m on (?P<month2>[0-9]+)/(?P<day2>[0-9]+)$'
        
        from_match = re.match(from_pattern, stipulation)
        if from_match is not None:
            hour = int(from_match.group('hour'))
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
            
            vehicle.available_from = available_from
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
            
            vehicle.available_until = available_until
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
            
            vehicle.available_from = available_from
            vehicle.available_until = available_until
            return
        
    
    def get_vehicle_from_html_data(self, pod, vehicle_info_div):
        vehicle_header = vehicle_info_div.find('h4')
        vehicle_name = vehicle_header.text
        
        availability_div = vehicle_info_div.find('div', {'class':'timestamp'})
        availability_p = availability_div.find('p')
        
        reserve_div = vehicle_info_div.find('div', {'class':'reserve'})
        reserve_a = reserve_div.find('a')
        lightbox_script = reserve_a['href']
        
        match = re.match(r"javascript:MV.controls.reserve.lightbox.create\('(?P<start_time>[0-9]*)', '(?P<end_time>[0-9]*)', '(?P<vehicle_id>[0-9]*)', ''\);", lightbox_script)
        vehicleid = match.group('vehicle_id')
        
        vehicle = Vehicle()
        vehicle.model = vehicle_name
        vehicle.pod = pod
        vehicle.id = vehicleid
        
        # Since the availability information is in the div too, store it.
        if availability_p['class'] == 'good':
            vehicle.availability = 1
        elif availability_p['class'] == 'bad':
            vehicle.availability = 0
        elif availability_p['class'] == 'maybe':
            vehicle.availability = 0.5
            self.assign_vehicle_availability_stipulation(vehicle, availability_p.text)
        
        return vehicle
    
    def create_vehicles_from_pcs_availability_doc(self, pcs_results_doc):
        vehicles = []
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
                vehicle = self.get_vehicle_from_html_data(current_pod, vehicle_div)
                vehicles.append(vehicle)
        
        return vehicles
    
    def create_host_connection(self):
        return PcsConnection()
    
    @override
    def get_available_vehicles_near(self, sessionid, locationid, start_time, end_time):
        conn = self.create_host_connection()
        
        pcs_available_body, pcs_available_headers = \
            self.availability_from_pcs(conn, sessionid, locationid, start_time, end_time)
        self._body = pcs_available_body
        self._headers = pcs_available_headers
        
        json_availability_data = self.get_json_data(pcs_available_body)
        html_pods_data = self.get_html_data(json_availability_data)
        
        vehicles = self.create_vehicles_from_pcs_availability_doc(html_pods_data)
        return vehicles
    
    def vehicle_info_from_pcs(self, conn, sessionid, vehicleid, start_time, end_time):
        host = self.__host
        path = self.__vehicle_path
        # The PhillyCarShare servers do not take into account time zone 
        # information in their timestamp calculations, so we have to reverse
        # our timezone info.  However, we have to keep it in the first place
        # because Google's servers aren't necessarily on Eastern time (but 
        # PhillyCarShare always will be).
        start_stamp = time.mktime((start_time - Eastern.utcoffset(start_time)).timetuple())
        end_stamp = time.mktime((end_time - Eastern.utcoffset(end_time)).timetuple())
        
        url = 'http://%s%s' % (host, path)
        method = 'POST'
        data = urllib.urlencode({'mv_action':'add',
                'default[stack_pk]':vehicleid,
                'default[start_stamp]':str(int(start_stamp)),
                'default[end_stamp]':str(int(end_stamp))})
        headers = { 'Cookie':'sid=%s' % sessionid }
        response = \
            conn.request(url, method, data, headers)
        
        return response.read(), response.getheaders()
    
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
        
        vehicle_model = model_tag.text
        
        vehicle = Vehicle()
        vehicle.model = vehicle_model
        vehicle.id = vehicleid
        return vehicle
    
    @override
    def get_vehicle(self, sessionid, vehicleid, start_time, end_time):
        conn = self.create_host_connection()
        
        pcs_vehicle_body, pcs_vehicle_headers = \
            self.vehicle_info_from_pcs(conn, sessionid, vehicleid, start_time, end_time)
        html_vehicle_data = self.get_html_vehicle_data(pcs_vehicle_body)
        
        vehicle = self.create_vehicle_from_pcs_information_doc(html_vehicle_data)
        return vehicle
    
    @override
    def get_vehicle_price_estimate(self, sessionid, vehicleid, start_time, end_time):
        return ''
