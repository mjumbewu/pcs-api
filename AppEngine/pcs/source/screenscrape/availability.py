import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from pcs.source import _AvailabilitySourceInterface
from util.abstract import override
from util.BeautifulSoup import BeautifulSoup

class AvailabilityScreenscrapeSource (_AvailabilitySourceInterface):
    """
    Responsible for logging in and constructing a session from a screenscrape
    of a PhillyCarShare response.
    """
    SIMPLE_FAILURE_DOCUMENT = "<html><head><title>Please Login</title></head><body></body></html>"
    
    def __init__(self, host="reservations.phillycarshare.org",
                 path="/results.php"):
        super(AvailabilityScreenscrapeSource, self).__init__()
        self.__host = host
        self.__path = path
    
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
    
    def create_vehicles_from_html_pod_data(self, html_data):
        pass
    
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
        
        vehicles = self.create_vehicles_from_html_pod_data(html_pods_data)
        return vehicles
