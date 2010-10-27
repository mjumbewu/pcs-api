import unittest
import datetime
import new

from util.testing import Stub
from util.testing import StubException
class StubTest (unittest.TestCase):
    
    def testShouldAcceptWhenMethodSignaturesAreIdenticalRegardlessOfAdditionalMethods(self):
        """Should accept when method signatures are identical regardless of additional methods"""
        # Given...
        class Real (object):
            def x(self, a, b=2):
                return a+b
            
            def y(self, c):
                return c
        
        # When...
        try:
            class Fake (object):
                def x(self, a, b=2):
                    return 5
            Fake = Stub(Real)(Fake)
            
        # Then...
        except StubException, e:
            self.fail('Fake should not cause a StubException: %s' % e.msg)
    
    def testShouldErrorWhenDifferentInstanceMethodParametersAreGiven(self):
        """Should raise an error when different instance method arguments are given"""
        # Given...
        class Real (object):
            x = 5
            def y(self, z):
                return x
        
        # When...
        try:
            class Fake (object):
                x = 4
                def y(self, a):
                    return 5
            Fake = Stub(Real)(Fake)
        
        # Then...
        except StubException:
            return
        
        # ...(fail if no exception)
        self.fail('Fake.y should not be a valid stub method')
    
    def testShouldErrorWhenStubMethodDoesNotExistInRealClass(self):
        """Should raise an error when a stub method does not exist in the real class"""
        # Given...
        class Real (object):
            pass
        
        # When...
        try:
            class Fake (object):
                def y(self, a):
                    pass
            Fake = Stub(Real)(Fake)
        
        # Then...
        except StubException:
            return
        
        self.fail('Fake.y should not be a valid stub method')
    
    def testErrorWhenStubbingVairablesThatDoNotExistInRealClass(self):
        """Should raise an error when creating variables that are not in the real class."""
        # Given...
        class Real (object):
            pass
        
        # When...
        try:
            class Fake (object):
                x = 'hello'
            Fake = Stub(Real)(Fake)
        
        # Then...
        except StubException:
            return
            
        self.fail('Fake.x should not be a valid stub class variable')
    
    def testShouldErrorWhenStubbingVariablesChangesVariableType(self):
        """Should raise an error when a variable in the stub class does not match type of the variable in the main class"""
        # Given...
        class Real (object):
            x = 5
        
        # When...
        try:
            class Fake (object):
                x = 'hello'
            Fake = Stub(Real)(Fake)
        
        # Then...
        except StubException:
            return
        
        self.fail('Fake.x should not be allowed to change variable type')
    
    def testShouldAcceptStubClassThatStubsVariables(self):
        """Should accept a stub class that uses a variable that is a stubbed version of a variable used in the real class"""
        # Given...
        class Var (object):
            pass
        
        class Real (object):
            x = Var()
        
        # When...
        class StubVar (object):
            pass
        StubVar = Stub(Var)(StubVar)
        
        try:
            class Fake(object):
                x = StubVar()
            Fake = Stub(Real)(Fake)
        
        # Then...
        except StubException:
            self.fail('Fake should be a valid stub')

