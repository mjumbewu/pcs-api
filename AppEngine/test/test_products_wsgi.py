import unittest

import util.testing

from crowdmkt.wsgi.product import ProductListHandler

class RequestStub (object):
    """
    A stub that provides context for a handler.
    
    Why stub?  Because a request normally comes from the WSGIApplication (which
    gets it from God knows where).  The request is the minimal interface between
    the handler and the user.
    """
    
    def __init__(self, args={}):
        self.__args = args
    
    def get(self, arg_name, default=''):
        return self.__args.get(arg_name, default)

class ResponseStub (object):
    """
    A stub that stores the state expected to result from using a response object.
    
    Why stub?  Because the response is normally created by the WSGIApplication,
    and we're not creating a WSGIApplication for the tests.
    """
    
    class OutputStub (object):
        def __init__(self):
            self.buffer = ''
        
        def write(self, output):
            self.buffer += output
    
    def __init__(self):
        self.out = self.OutputStub()
        self.status = None
    
    def set_status(self, value):
        self.status = value
    
    def clear(self):
        self.out.buffer = ''


class ProductListHandler_GET_TestCase (unittest.TestCase):
    
    def setUp(self):
        # Create a stub for the ProductListFetcher that "retrieves" some bogus
        # products.
        from crowdmkt.db.product import ProductListFetcher
        def ProductListFetcherStub():
            """This factory creates a product list fetcher, but patches the 
            get_products method with a stub.
            """
            fetcher = ProductListFetcher()
            def get_products(self, count):
                return ["product"+str(i) for i in xrange(count)]
            util.testing.patch(fetcher, get_products)
            return fetcher
        
        # Create a stub for the ProductListSerializer that returns some canned 
        # output.
        from crowdmkt.wsgi.product import ProductListSerializer
        def ProductListSerializerStub():
            """This factory creates a product list serializer, but patches the 
            get_xml method with a stub.
            """
            serializer = ProductListSerializer()
            def get_xml(self, products):
                return ','.join(products)
            util.testing.patch(serializer, get_xml)
            return serializer
        
        # Set up a response stub to catch the handler response, and patch it onto
        # the handler.    Make the ResponseStub object an instance variable so that
        # we can check the state in our assertions.
        self.response = ResponseStub()
        self.handler = ProductListHandler(ProductListFetcherStub,
                                          ProductListSerializerStub)
        self.handler.response = self.response
        
    def test1(self):
        """When you call 'get' on the ProductListHandler, the response should be filled with whatever comes from the product serializer."""
        
        self.handler.request = RequestStub({'count':'5'})
        self.handler.get()
        
        xml = "product0,product1,product2,product3,product4"
        status = 200
        
        self.assertEqual(self.response.out.buffer, xml, 
            "Expected xml: %r.    Recieved: %r" % 
            (xml, self.response.out.buffer))
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.    Received: %r" % 
            (status, self.response.status))
    
    def test2(self):
        """When 3 products are requested without a skip parameter, first 3 products are serialized and returned."""
        
        self.handler.request = RequestStub({ 'count' : '3' })
        self.handler.get()
        
        xml = "product0,product1,product2"
        status = 200
        
        self.assertEqual(self.response.out.buffer, xml,
            "Expected xml: %r.    Received: %r" %
            (xml, self.response.out.buffer))
        self.assertEqual(self.response.status, status,
            "Expected status: %r. Received: %r" %
            (status, self.response.status))
    
    def test3(self):
        """When no value is supplied for the product count, the handler will return a 400 status with an error string describing the problem.    The number of products to return is a required argument."""
        
        self.handler.request = RequestStub()
        self.handler.get()
        
        status = 400
        
        self.assertEqual(self.response.status, status,
            "Expected status: %r.    Received: %r" %
            (status, self.response.status))
        self.assertNotEqual(self.response.out.buffer, '',
            "The response body should not be empty.")
    

class ProductListHandler_POST_TestCase (unittest.TestCase):
    
    def setUp(self):
        # Create a stub for the ProductListFetcher that "retrieves" some bogus
        # products.
        from crowdmkt.db.product import ProductListFetcher
        def ProductListFetcherStub():
            fetcher = ProductListFetcher()
            def get_products(self, count):
                return ["product"+str(i) for i in xrange(count)]
            util.testing.patch(fetcher, get_products)
            return fetcher
        
        # Create a stub for the ProductListSerializer that returns some canned 
        # output.
        from crowdmkt.wsgi.product import ProductListSerializer
        def ProductListSerializerStub():
            serializer = ProductListSerializer()
            def get_xml(self, products):
                return ','.join(products)
            util.testing.patch(serializer, get_xml)
            return serializer
        
        # Set up a response stub to catch the handler response, and patch it onto
        # the handler.    Make the ResponseStub object an instance variable so that
        # we can check the state in our assertions.
        self.response = ResponseStub()
        self.handler = ProductListHandler(ProductListFetcherStub,
                                          ProductListSerializerStub)
        self.handler.response = self.response
        
        # Initialize the product model buffer mock.
        self.product_model_buffer = self.ProductModelBuffer()
        self.ProductModelStub.buffer = self.product_model_buffer
        
    class ProductModelBuffer (object):
        name = None
        brand = None
        foods = None
        manufacturer = None
        size = None
        unit = None
    
    class ProductModelStub (object):
        """A stub product model that reads to/writes from a buffer.
        
        The actual ProductModel interacts with the datastore when created, so
        we don't want to derive from it.
        """
        buffer = None
        
        @property
        def name(self):
            return self.buffer.name
        @name.setter
        def name(self, value):
            self.buffer.name = value
        
        @property
        def brand(self):
            return self.buffer.brand
        @brand.setter
        def brand(self, value):
            self.buffer.brand = value
        
        @property
        def foods(self):
            return self.buffer.foods
        @foods.setter
        def foods(self, value):
            self.buffer.foods = value
        
        @property
        def manufacturer(self):
            return self.buffer.manufacturer
        @manufacturer.setter
        def manufacturer(self, value):
            self.buffer.manufacturer = value
        
        @property
        def size(self):
            return self.buffer.size
        @size.setter
        def size(self, value):
            self.buffer.size = value
        
        @property
        def unit(self):
            return self.buffer.unit
        @unit.setter
        def unit(self, value):
            self.buffer.unit = value
        
        def key(self):
            return 'productkey'
    
    class BrandModelStub (object):
        @classmethod
        def get(cls, key):
            if key == 'brandkey':
                return cls()
            else:
                return None
        
        def key(self):
            return 'brandkey'
    
    class ManufacturerModelStub (object):
        @classmethod
        def get(cls, key):
            if key == 'mfctkey':
                return cls()
            else:
                return None
        
        def key(self):
            return 'mfctkey'
    
    class FoodModelStub (object):
        @classmethod
        def get(cls, key):
            if key == 'foodkey1' or key == 'foodkey2':
                return cls()
            else:
                return None
    
    def test4(self):
        """When minimal required arguments are given in the request, a product entry should be created and the response should be filled with the product's identifier."""
        
        self.handler.request = RequestStub({
            'name' : 'productname'
        })
        self.handler.post(self.ProductModelStub, self.BrandModelStub, 
                          self.FoodModelStub, self.ManufacturerModelStub)
        
        status = 200
        key = 'productkey'
        
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.  Received: %r" %
            (status, self.response.status))
        self.assertEqual(self.response.out.buffer, key,
            "Expected response: %r.  Received: %r" %
            (key, self.response.out.buffer))
    
    def test5(self):
        """When name is not provided as an argument, a 400 status and an informative response message should be returned."""
        
        self.handler.request = RequestStub({
            'foods' : '["foodkey1","foodkey2"]',
            'brand' : 'brandkey',
            'manufacturer' : 'mfctkey',
            'size' : '10',
            'unit' : 'tbsp'
        })
        self.handler.post(self.ProductModelStub, self.BrandModelStub, 
                          self.FoodModelStub, self.ManufacturerModelStub)
        
        status = 400
        
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.  Received: %r" %
            (status, self.response.status))
        self.assertNotEqual(self.response.out.buffer, '',
            "Response message should not be empty")
    
    def test6(self):
        """When a name is given, it should be set on the product model correctly.  Other parameters should be set correctly as well."""
        
        self.handler.request = RequestStub({
            'name' : 'product name',
            'foods' : '["foodkey1","foodkey2"]',
            'brand' : 'brandkey',
            'manufacturer' : 'mfctkey',
            'size' : '10',
            'unit' : 'tbsp'
        })
        self.handler.post(self.ProductModelStub, self.BrandModelStub, 
                          self.FoodModelStub, self.ManufacturerModelStub)
        
        status = 200
        name = 'product name'
        brandkey = 'brandkey'
        foodcount = 2
        mfctkey = 'mfctkey'
        size = 10
        unit = 'tbsp'
        
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.  Received: %r" %
            (status, self.response.status))
        self.assertEqual(self.product_model_buffer.name, name, 
            "Expected name: %r.  Received: %r" %
            (name, self.product_model_buffer.name))
        self.assertEqual(self.product_model_buffer.brand.key(), brandkey,
            "Expected brand key: %r.  Received: %r" %
            (brandkey, self.product_model_buffer.brand.key()))
        self.assertEqual(len(self.product_model_buffer.foods), foodcount,
            "Expected %r foods.  Received: %r" %
            (foodcount, self.product_model_buffer.foods))
        self.assertEqual(self.product_model_buffer.manufacturer.key(), mfctkey,
            "Expected manufacturer key: %r.  Received: %r" %
            (mfctkey, self.product_model_buffer.manufacturer.key()))
        self.assertEqual(self.product_model_buffer.size, size,
            "Expected size: %r.  Recieved: %r" %
            (size, self.product_model_buffer.size))
        self.assertEqual(self.product_model_buffer.unit, unit,
            "Expected unit: %r.  Recieved: %r" %
            (unit, self.product_model_buffer.unit))
    
    def test7(self):
        """When a brand is given, but it does not exist, a 400 status with appropriate error message is returned."""
        
        self.handler.request = RequestStub({
            'name' : 'product name',
            'foods' : '["foodkey1","foodkey2"]',
            'brand' : 'unknown',
            'manufacturer' : 'mfctkey',
            'size' : '10',
            'unit' : 'tbsp'
        })
        self.handler.post(self.ProductModelStub, self.BrandModelStub, 
                          self.FoodModelStub, self.ManufacturerModelStub)
        
        status = 400
        signature = 'Brand'
        
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.  Received: %r" %
            (status, self.response.status))
        self.assert_(signature in self.response.out.buffer, 
            "Expected the string %r to be in the output.  Received: %r" %
            (signature, self.response.out.buffer))
    
    def test8(self):
        """When a food is given, but it does not exist, a 400 status with appropriate error message is returned."""
        
        self.handler.request = RequestStub({
            'name' : 'product name',
            'foods' : '["foodkey1","unknown"]',
            'brand' : 'brandkey',
            'manufacturer' : 'mfctkey',
            'size' : '10',
            'unit' : 'tbsp'
        })
        self.handler.post(self.ProductModelStub, self.BrandModelStub, 
                          self.FoodModelStub, self.ManufacturerModelStub)
        
        status = 400
        signature = 'food'
        
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.  Received: %r" %
            (status, self.response.status))
        self.assert_(signature in self.response.out.buffer, 
            "Expected the string %r to be in the output.  Received: %r" %
            (signature, self.response.out.buffer))
    
    def test9(self):
        """When a manufacturer is given, but it does not exist, a 400 status with appropriate error message is returned."""
        
        self.handler.request = RequestStub({
            'name' : 'product name',
            'foods' : '["foodkey1","foodkey2"]',
            'brand' : 'brandkey',
            'manufacturer' : 'unknown',
            'size' : '10',
            'unit' : 'tbsp'
        })
        self.handler.post(self.ProductModelStub, self.BrandModelStub, 
                          self.FoodModelStub, self.ManufacturerModelStub)
        
        status = 400
        signature = 'Manufacturer'
        
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.  Received: %r" %
            (status, self.response.status))
        self.assert_(signature in self.response.out.buffer, 
            "Expected the string %r to be in the output.  Received: %r" %
            (signature, self.response.out.buffer))
    
    def test10(self):
        """When a non-list foods is given, set a 400 status and an appropriate response message"""
        
        self.handler.request = RequestStub({
            'name' : 'product name',
            'foods' : '["unknown","foodkey2"]',
            'brand' : 'brandkey',
            'manufacturer' : 'mfctkey',
            'size' : '10',
            'unit' : 'tbsp'
        })
        self.handler.post(self.ProductModelStub, self.BrandModelStub, 
                          self.FoodModelStub, self.ManufacturerModelStub)
        
        status = 400
        signature = 'A food'
        
        self.assertEqual(self.response.status, status, 
            "Expected status: %r.  Received: %r" %
            (status, self.response.status))
        self.assert_(signature in self.response.out.buffer, 
            "Expected the string %r to be in the output.  Received: %r" %
            (signature, self.response.out.buffer))
        

class ProductApplication_TestCase (unittest.TestCase):
    def test1(self):
        """When a ProductListHandler is constructed without any parameters, it should have a fetcher of type crowdmkt.db.product.ProductListFetcher and a serializer of type crowdmkt.wsgi.product.ProductListSerializer
        
        This is necessary because the application does not pass any parameters to 
        the constructor.
        """
        
        handler = ProductListHandler()
        
        fetcher = handler._ProductListHandler__fetcher
        serializer = handler._ProductListHandler__serializer
        
        import crowdmkt.db.product
        import crowdmkt.wsgi.product
        
        self.assert_(isinstance(fetcher, crowdmkt.db.product.ProductListFetcher))
        self.assert_(isinstance(serializer, crowdmkt.wsgi.product.ProductListSerializer))

