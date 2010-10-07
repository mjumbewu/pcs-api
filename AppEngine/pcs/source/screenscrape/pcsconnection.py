import httplib

from google.appengine.api.urlfetch import DownloadError 

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
            conn = httplib.HTTPConnection(host)
        elif scheme == self.HTTPS:
            conn = httplib.HTTPSConnection(host)
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
    
    def __request_helper(self, url, method, data, headers, follow_count=5, retry_count=3):
        try:
            scheme, host, path = self.parse_url(url)
            conn = self.create_host_connection(scheme, host)
            self.make_request(conn, method, path, data, headers)
            
            initial_response = self.get_response(conn)
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
        return self.__request_helper(url, method, data, headers, 5, 3)

