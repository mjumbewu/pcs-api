import httplib

from google.appengine.api.urlfetch import DownloadError 
from google.appengine.api.urlfetch import fetch as gaefetch

class PcsConnectionError (Exception):
    pass

class PcsConnection (object):

    HTTP = 'http'
    HTTPS = 'https'
    
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    
    def parse_url(self, url):
        try:
            scheme_end = url.find('://')
            if scheme_end == -1:
                raise PcsConnectionError('Unparsable url: %r' % url)
            scheme = url[:scheme_end]
            location = url[scheme_end+3:]
            
            host_end = location.find('/')
            if host_end == -1:
                raise PcsConnectionError('Unparsable url: %r' % url)
            host = location[:host_end]
            path = location[host_end:]
            
            return (scheme, host, path)
        except IndexError:
            raise PcsConnectionError('Unparsable url: %r' % url)
    
    def create_host_connection(self, scheme, host):
        if scheme == self.HTTP:
            conn = httplib.HTTPConnection(host, timeout=10)
        elif scheme == self.HTTPS:
            conn = httplib.HTTPSConnection(host, timeout=10)
        else:
            raise PcsConnectionError('Unrecognized connection scheme: %r' % scheme)
        
        return conn
    
    def make_request(self, conn, method, path, data, headers):
        if method not in (self.GET, self.PUT, self.POST, self.DELETE):
            raise PcsConnectionError('Unrecognized connection method: %r' % method)
        
        conn.request(method, path, data, headers)
    
    def get_response(self, conn):
        return conn.getresponse()
    
    def follow_if_redirect(self, response, method, data, headers, follow_count):
        if response.status in (301, 302) and follow_count > 0:
            location = response.getheader('location')
            return self.__request_helper(location, method, data, headers, follow_count-1)
        return response
    
    def request_with_httplib(self, url, method, data, headers):
        scheme, host, path = self.parse_url(url)
        conn = self.create_host_connection(scheme, host)
        self.make_request(conn, method, path, data, headers)
        
        response = self.get_response(conn)
        return response
        
    def request_with_gae(self, url, method, data, headers):
        """Request the resource using GAE's fetch.
        
        I use this method so that I can be more sure that GAE is paying 
        attention to my timeout deadline.  If I weren't using GAE, I'd use the
        other request method (e.g., from a Django instance).
        """
        
        response = gaefetch(url, data, method, headers, follow_redirects=False, deadline=10)
        
        # Wrap the response to make it look like an HTTPResponse object
        class ResponseWrapper (object):
            def __init__(self, gae_response):
                self.gae_response = gae_response
            
            @property
            def status(self):
                return self.gae_response.status_code
            
            def read(self):
                return self.gae_response.content
            
            def getheaders(self):
                return self.gae_response.headers
            
            def getheader(self, header):
                return self.gae_response.headers[header]
        
        wrapped_response = ResponseWrapper(response)
        return wrapped_response
    
    def __request_helper(self, url, method, data, headers, follow_count=5, retry_count=3):
        try:
            initial_response = self.request_with_gae(url, method, data, headers)
#            initial_response = self.request_with_httplib(url, method, data, headers)
            final_response = self.follow_if_redirect(initial_response, method, 
                data, headers, follow_count)
            return final_response
        except DownloadError, de:
            if retry_count > 0:
                return self.__request_helper(url, method, data, headers, follow_count, retry_count-1)
            else:
                raise PcsConnectionError('Failed to connect to %s after max retry count: %s' % (url, de))
    
    def request(self, url, method, data, headers):
        """
        This should be the only method in the public interface.  Get a response
        from the given url, following any redirects.
        """
        return self.__request_helper(url, method, data, headers, 5, 0)

