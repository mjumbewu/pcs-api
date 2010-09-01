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
from pcs.source import _AvailabilitySourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup
from util.TimeZone import Eastern

class AvailabilityScreenscrapeSource (_AvailabilitySourceInterface):
    """
    Responsible for logging in and constructing a session from a screenscrape
    of a PhillyCarShare response.
    """
    SIMPLE_FAILURE_DOCUMENT = "<html><head><title>Please Login</title></head><body></body></html>"
    
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/results.php?reservation_id=0&flexible=on&show_everything=on&offset=0"):
        super(AvailabilityScreenscrapeSource, self).__init__()
        self.__host = host
        self.__path = path
    
    def get_location_query(self, location):
        if isinstance(location, (basestring, int)):
            query = 'location=driver_locations_%s' % location
            return query
        
        if isinstance(location, (list, tuple)) and len(location) == 2:
            latitude = location[0]
            longitude = location[1]
            query = 'location_latitude=%s&location_longitude=%s' % \
                (latitude, longitude)
            return query
        
        raise Exception('unrecognizable location: %r' % location)
    
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
    
    def availability_from_pcs(self, conn, sessionid, location, start_time, end_time):
        """
        Attempts to load a session from the connection with the given session
        id.
        
        @return: The server response.  If reconnection failed, the response
          body should be identifiable as an invalid session.
        """
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        query = self.get_location_query(location)
        query += '&' + self.get_time_query(start_time, end_time)
        connector = '&' if '?' in self.__path else '?'
        conn.request("GET", self.__path + connector + query,
            {}, headers)
        
        try:
            response = conn.getresponse()
        except:
            return (self.SIMPLE_FAILURE_DOCUMENT, [])
        
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
        pod_link = pod_info_div.findAll('a')[0]
        
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
        vehicle_header = vehicle_info_div.findAll('h4')[0]
        vehicle_name = vehicle_header.text
        
        availability_div = vehicle_info_div.findAll('div', {'class':'timestamp'})[0]
        availability_p = availability_div.findAll('p')[0]
        
        vehicle = Vehicle(vehicle_name, pod)
        
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
        
        bodies = pcs_results_doc.findAll('body')
        body = bodies[0]
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
        return httplib.HTTPConnection(self.__host)
    
    @override
    def get_available_vehicles_near(self, sessionid, location, start_time, end_time):
        conn = self.create_host_connection()
        
        pcs_available_body, pcs_available_headers = \
            self.availability_from_pcs(conn, sessionid, location, start_time, end_time)
        self._body = pcs_available_body
        self._headers = pcs_available_headers
        
        json_availability_data = self.get_json_data(pcs_available_body)
        html_pods_data = self.get_html_data(json_availability_data)
        
        vehicles = self.create_vehicles_from_pcs_availability_doc(html_pods_data)
        return vehicles
