import inspect
import new

class StubException (Exception):
    pass

class Stub (object):
    """
    A decorator for creating a stub class
    """
    
    def __init__(self, real_cls):
        self.real_cls = real_cls
    
    def invalid_reason(self, stub_cls, member_name):
        """
        Return a reason that the given member is not valid in the given stub
        class.  If the member is valid, return None.
        """
        stub_member = getattr(stub_cls, member_name)
        stub_member_type = type(stub_member)
        while hasattr(stub_member_type, '_stubbed_type'):
            stub_member_type = stub_member_type._stubbed_type
        
        # Fail if the real class does not have the member
        if not hasattr(self.real_cls, member_name):
            return '%s has no attribute %r' \
                % (self.real_cls.__name__, member_name)
        
        real_member = getattr(self.real_cls, member_name)
        real_member_type = type(real_member)
        
        # Fail if the types of the members differ
        if stub_member_type.__name__ != real_member_type.__name__:
            return 'Type mismatch for %s.%s' % (stub_cls.__name__, member_name)
        
        if stub_member_type.__name__ in ('instancemethod', 'function'):
            real_member_sig = inspect.getargspec(real_member)
            stub_member_sig = inspect.getargspec(stub_member)
            
            # Fail if they're functions with different signatures
            if real_member_sig != stub_member_sig:
                return 'Member functions have different signatures.'
        
        # Otherwise, pass
        return None
    
    def verify_stub_class(self, stub_cls):
        """
        Verify that the stub class is a valid stub for the real class.
        """
        real_members = dir(self.real_cls)
        stub_members = dir(stub_cls)
        
        for member_name in stub_members:
            invalid_reason = self.invalid_reason(stub_cls, member_name)
            if invalid_reason is not None:
                raise StubException('%s.%s is not a valid stub: %s' 
                    % (stub_cls.__name__, member_name, invalid_reason))
    
    def mark_as_stub_class(self, stub_cls):
        """
        Mark the given stub class as a stub of the real class.
        """
        stub_cls._stubbed_type = self.real_cls
        
    def __call__(self, stub_cls):
        self.verify_stub_class(stub_cls)
        self.mark_as_stub_class(stub_cls)
        return stub_cls

#class Dec (object):
#    def __init__(self, f):
#        self.f = f
#        self.__name__ = f.__name__
#        self.__doc__ = f.__doc__
#    
#    def __call__(self, *args):
#        return f

#class A (object):
#    @Dec
#    def x(self):
#        pass

