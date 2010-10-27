import unittest
import datetime
import new

from util.abstract import override
from util.abstract import OverrideException
class OverrideTest (unittest.TestCase):
    
    def testShouldAcceptWhenMethodParametersAreIdentical(self):
        # Given...
        class Base (object):
            def x(self, a, b=2):
                return a+b
            
            def y(self, c):
                return c
        
        class Derived (Base):
            @override
            def x(self, a, b):
                return 5
        
        # When...
        try:
            i = Derived()
            i.x(1,2)
            
        # Then...
        except OverrideException, e:
            self.fail('Derived.x should not cause an OverrideException: %s' % e.msg)
    
    def testShouldErrorWhenMethodParametersAreDifferent(self):
        # Given...
        class Base (object):
            def x(self, a, b=2):
                return a+b
            
            def y(self, c):
                return c
        
        class Derived (Base):
            @override
            def x(self, a):
                return 5
        
        # When...
        try:
            i = Derived()
            i.x(1)
            
        # Then...
        except OverrideException, e:
            return
        
        self.fail('Derived.x should have caused an OverrideException.')

