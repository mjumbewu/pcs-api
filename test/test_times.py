import unittest
import datetime

from util.TimeZone import Eastern
from util.TimeZone import from_isostring

class from_isostringTest (unittest.TestCase):
    def testShouldRecognizeYMDHi(self):
        iso = "2010-11-12T06:15"
        expected = datetime.datetime(2010,11,12,6,15,tzinfo=Eastern)
        
        self.assertEqual(from_isostring(iso), expected)
    
    def testShouldRecognizeYMD(self):
        iso = "2010-11-12"
        expected = datetime.datetime(2010,11,12,tzinfo=Eastern)
        
        self.assertEqual(from_isostring(iso), expected)
    
    def testShouldRecognizeYM(self):
        iso = "2010-11"
        expected = datetime.datetime(2010,11,1,tzinfo=Eastern)
        
        self.assertEqual(from_isostring(iso), expected)
    
    def testShouldRecognizeY(self):
        iso = "2010"
        expected = datetime.datetime(2010,1,1,tzinfo=Eastern)
        
        self.assertEqual(from_isostring(iso), expected)
    

