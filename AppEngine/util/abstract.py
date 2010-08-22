import functools
import inspect
import new

class OverrideException (Exception):
    pass

def override(method):
    
    def invalid_reason(method, calling_inst):
        """
        Return a reason that the given overriden member is not valid in the 
        given class.  If the member is valid, return None.
        """
        parent_class = inspect.getmro(calling_inst.__class__)[1]
        
        if not hasattr(parent_class, method.__name__):
            return 'Parent class %s has no attribute %r' \
                % (parent_class.__name__, method.__name__)
        
        method_args = inspect.getargspec(method)
        parent_args = inspect.getargspec(getattr(parent_class, 
                                                 method.__name__))
        
        if method_args[0] != parent_args[0]:
            return 'Mismatched arguments'
        
        # Otherwise, pass
        return None
    
    def verify_against_calling_inst(calling_inst):
        reason = invalid_reason(method, calling_inst)
        if reason is not None:
            raise OverrideException('%s.%s is not a valid override: %s' 
                % (calling_inst.__class__.__name__, method.__name__, reason))
    
    @functools.wraps(method)
    def wrapped(self, *args, **kwds):
        verify_against_calling_inst(self)
        return method(self, *args, **kwds)
    
    return wrapped

#class override (object):
#    """
#    A decorator for creating a stub class
#    """
#    
#    def __init__(self, method):
#        self.method = method
#        self.__name__ = method.__name__
#        self.__doc__ = method.__doc__
#    
#    def invalid_reason(self, method, calling_inst):
#        """
#        Return a reason that the given overriden member is not valid in the 
#        given class.  If the member is valid, return None.
#        """
#        parent_class = inspect.getmro(calling_inst.__class__)[1]
#        
#        if not hasattr(parent_class, self.method.__name__):
#            return 'Parent class %s has no attribute %r' \
#                % (parent_class.__name__, self.method.__name__)
#        
#        method_args = inspect.getargspec(self.method)
#        parent_args = inspect.getargspec(getattr(parent_class, 
#                                                 self.method.__name__))
#        
#        if method_args[1] != parent_args[1]:
#            return 'Mismatched arguments'
#        
#        # Otherwise, pass
#        return None
#    
#    def verify_against_calling_inst(self, calling_inst):
#        invalid_reason = self.invalid_reason(self.method, calling_inst)
#        if invalid_reason is not None:
#            raise OverrideException('%s.%s is not a valid override: %s' 
#                % (calling_inst.__name__, self.method.__name__, invalid_reason))
#    
#    def __call__(self, wrapped_self, *args, **kwds):
##        self.verify_against_calling_inst(wrapped_self)
#        return self.method(*args, **kwds)

