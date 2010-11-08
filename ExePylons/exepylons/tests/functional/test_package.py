from exepylons.tests import *
from exepylons.tests.test_tools import *

class TestPackageController(TestController):
    
    def setUp(self):
        TestController.setUp(self)
        # Login as admin
        self.app.post(url(controller='login', action='submit'),
                      params={'login':'admin', 'password':'admin'})
        
    def test_index(self):
        response = self.app.get(url(controller='package', action='index', 
                                    packageId=1))
        # Test response...
        _assert_in(['Package 1'], response)
