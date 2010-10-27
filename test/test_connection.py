import unittest
import StringIO

from util.testing import Stub
from util.testing import patch

from pcs.source.screenscrape.pcsconnection import PcsConnection
from pcs.source.screenscrape.pcsconnection import PcsConnectionError
class PcsConnectionTest (unittest.TestCase):
    def testShouldParseUrlCorrectly1(self):
        conn = PcsConnection()
        url = 'http://www.google.com:8080/'
        
        scheme, host, path = conn.parse_url(url)
        
        self.assertEqual(scheme, PcsConnection.HTTP)
        self.assertEqual(host, 'www.google.com:8080')
        self.assertEqual(path, '/')
    
    def testShouldParseUrlCorrectly2(self):
        conn = PcsConnection()
        url = 'https://www.google.com/dir/index.php?arg=value'
        
        scheme, host, path = conn.parse_url(url)
        
        self.assertEqual(scheme, PcsConnection.HTTPS)
        self.assertEqual(host, 'www.google.com')
        self.assertEqual(path, '/dir/index.php?arg=value')
    
    def testInvalidUrlShouldRaiseException1(self):
        conn = PcsConnection()
        url = 'http:/www.google.com/'
        
        try:
            scheme, host, path = conn.parse_url(url)
        
        except PcsConnectionError:
            return
        
        self.fail('Should not parse invalid url %r as %r' % (url, [scheme, host, path]))
    
    def testInvalidUrlShouldRaiseException2(self):
        conn = PcsConnection()
        url = 'http://www.google.com'
        
        try:
            scheme, host, path = conn.parse_url(url)
        
        except PcsConnectionError:
            return
        
        self.fail('Should not parse invalid url %r as %r' % (url, [scheme, host, path]))
    
    def testShouldCreateHttpConnectiomFromHttpScheme(self):
        conn = PcsConnection()
        
        http_conn = conn.create_host_connection('http', 'localhost')
        
        self.assertEqual(http_conn.__class__.__name__, 'HTTPConnection')
    
    def testShouldCreateHttpsConnectiomFromHttpsScheme(self):
        conn = PcsConnection()
        
        https_conn = conn.create_host_connection('https', 'localhost')
        
        self.assertEqual(https_conn.__class__.__name__, 'HTTPSConnection')

