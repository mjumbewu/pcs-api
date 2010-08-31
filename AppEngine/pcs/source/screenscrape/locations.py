import httplib
import re
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from pcs.data.location import LocationProfile
from pcs.data.location import LocationCoordinate
from pcs.source import _LocationsSourceInterface
from pcs.source.screenscrape import ScreenscrapeParseError
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup

class LocationsScreenscrapeSource (_LocationsSourceInterface):
    """
    Responsible for constructing a set of location profiles from a screenscrape
    of a PhillyCarShare response.
    """
    SIMPLE_FAILURE_DOCUMENT = "<html><head><title>Please Login</title></head><body></body></html>"
    
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/my_info.php?mv_action=dpref&pk=6285506&mvssl"):
        super(LocationsScreenscrapeSource, self).__init__()
        self.__host = host
        self.__prefs_path = path
    
    def create_connection(self):
        conn = httplib.HTTPConnection(self.__host)
        conn._follow_redirects = True
        return conn
    
    def get_preferences_response(self, conn, sessionid):
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        conn.request('GET', self.__prefs_path, {}, headers)
        try:
            response = conn.getresponse()
        except:
            return (self.SIMPLE_FAILURE_DOCUMENT, {})
        
        return (response.read(), response.getheaders())
    
    def parse_locations_from_preferences_body(self, response_body):
        location_profiles = []
        
        response_doc = BeautifulSoup(response_body)
        tbody_tags = response_doc.findAll('tbody', 
            {'id':'dpref_driver_pk__preferences_pk__driver_locations_pk__profiles'})
        
        if len(tbody_tags) == 0:
            raise ScreenscrapeParseError('No tbody found: %r' % response_body)
        
        tbody_tag = tbody_tags[0]
        
        tr_tags = tbody_tag.findAll('tr')
        for tr_tag in tr_tags:
            profile_name_td_tag = tr_tag.findAll('td', {'class':'profile_name'})[0]
            profile_desc_td_tag = tr_tag.findAll('td', {'class':'profile_descr'})[0]
            profile_id_td_tag = tr_tag.findAll('input', {'class':'profile_default'})[0]
            
            profile_name = profile_name_td_tag.text
            profile_desc = profile_desc_td_tag.text
            profile_id = profile_id_td_tag['value']
            
            location_profile = LocationProfile(profile_name,
                                      profile_id,
                                      profile_desc)
            location_profiles.append(location_profile)
        
        return location_profiles
    
    @override
    def get_location_profiles(self, sessionid):
        conn = self.create_connection()
        locations = None
        prefs_body, prefs_headers = \
            self.get_preferences_response(conn, sessionid)
        locations = self.parse_locations_from_preferences_body(prefs_body)
        
        return locations
    
    @override
    def get_location_profile(self, sessionid, locationid):
        conn = self.create_connection()
        locations = self.get_location_profiles(sessionid)
        
        for location in locations:
            if location.id == locationid:
                return location
        
        raise ScreenscrapeParseError('No location with id %r found' % locationid)
    
    @override
    def get_custom_location(self, location_name, location_key):
        if not isinstance(location_key, (list, tuple)) or len(location_key) != 2:
            raise ScreenscrapeParseError('Invalid location key: %r' % location_key)
        
        location = LocationCoordinate(location_name, *location_key)
        return location
    
    def availability_from_pcs(self, conn, sessionid, location, start_time, end_time):
        """
        Attempts to load a session from the connection with the given session
        id.
        
        @return: The server response.  If reconnection failed, the response
          body should be identifiable as an invalid session.
        """
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        conn.request("POST", self.__path,
            {}, headers)
        conn._follow_redirects = True
        
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
        pod_divs = json_data['pods']
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
    
    def get_vehicle_from_html_data(self, pod, vehicle_info_div):
        vehicle_header = vehicle_info_div.findAll('h4')[0]
        
        vehicle_name = vehicle_header.text
        
        vehicle = Vehicle(vehicle_name, pod)
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
