import unittest

import util.restful
import util.testing

class patch_TestCase (unittest.TestCase):
    def test1(self):
        """Patching a class with an existing method should be fine."""
        class A (object):
            def x(self):
                return 0
        
        a = A()
        def x(self):
            return 5
        util.testing.patch(a, x)
        
        self.assertEqual(a.x(), x(a))
    
    def test2(self):
        """Patching a class without an existing method should raise an assertion."""
        class A (object):
            def x(self):
                pass
        
        a = A()
        def y(self):
            return 6
        
        self.assertRaises(AttributeError, util.testing.patch, a, y)

class parse_arg_TestCase (unittest.TestCase):
    
    def test3(self):
        """Passing in a string that begins with an open square-bracket will cause the string to be parsed as a list (in JSON syntax)."""
        result = util.restful.parse_arg('["elem1","elem2"]')
        
        self.assertEqual(result, ['elem1','elem2'])
    
    def test4(self):
        """Passing in a string that is enclosed in quotes will cause the string to be parsed as a string (in JSON syntax)."""
        result = util.restful.parse_arg('"hello"')
        
        self.assertEqual(result, 'hello')
    
    def test5(self):
        """Passing in a string that is a number will cause the string to be parsed as a number (in JSON syntax)."""
        result = util.restful.parse_arg('7.2')
        
        self.assertEqual(result, 7.2)
    
    def test6(self):
        """Passing in a string that can't be interpreted as a JSON string will just return the string."""
        result = util.restful.parse_arg('hello')
        
        self.assertEqual(result, 'hello')
    
