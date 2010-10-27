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
from pcs.fetchers import _LocationsSourceInterface
from pcs.fetchers.screenscrape import ScreenscrapeParseError
from pcs.fetchers.screenscrape.pcsconnection import PcsConnection
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup

class LocationsScreenscrapeSource (_LocationsSourceInterface):
    """
    Responsible for constructing a set of location profiles from a screenscrape
    of a PhillyCarShare response.
    """
    SIMPLE_FAILURE_DOCUMENT = "<html><head><title>Please Login</title></head><body></body></html>"
    
    def __init__(self, url="http://reservations.phillycarshare.org/my_info.php?mv_action=dpref&mvssl"):
        super(LocationsScreenscrapeSource, self).__init__()
        self.__url = url
    
    def create_connection(self):
        conn = PcsConnection()
        return conn
    
    def get_preferences_response(self, conn, sessionid):
        headers = {
            'Cookie': 'sid=%s' % sessionid}
        response = conn.request(self.__url, 'GET', {}, headers)
        return (response.read(), response.getheaders())
    
    def parse_locations_from_preferences_body(self, response_body):
        location_profiles = []
        
        response_doc = BeautifulSoup(response_body)
        tbody_tag = response_doc.find('tbody', 
            {'id':'dpref_driver_pk__preferences_pk__driver_locations_pk__profiles'})
        
        if tbody_tag is None:
            raise ScreenscrapeParseError('No tbody found: %r' % response_body)
        
        tr_tags = tbody_tag.findAll('tr')
        for tr_tag in tr_tags:
            profile_name_td_tag = tr_tag.findAll('td', {'class':'profile_name'})[0]
            profile_desc_td_tag = tr_tag.findAll('td', {'class':'profile_descr'})[0]
            profile_id_radio_tag = tr_tag.findAll('input', {'class':'profile_default'})[0]
            
            profile_name = profile_name_td_tag.text
            profile_desc = profile_desc_td_tag.text
            profile_id = profile_id_radio_tag['value']
            profile_def = (profile_id_radio_tag.get('checked',None) == 'checked')
            
            location_profile = LocationProfile(profile_name,
                                      profile_id,
                                      profile_desc)
            location_profile.is_default = profile_def
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
            if locationid is None and location.is_default:
                return location
            elif location.id == locationid:
                return location
        
        raise ScreenscrapeParseError('No location with id %r found' % locationid)
    
    @override
    def get_custom_location(self, location_name, location_key):
        if not isinstance(location_key, (list, tuple)) or len(location_key) != 2:
            raise ScreenscrapeParseError('Invalid location key: %r' % location_key)
        
        location = LocationCoordinate(location_name, *location_key)
        return location

