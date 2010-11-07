from exepylons.tests import *
from exepylons.tests.test_tools import assert_in

class TestPackageController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='package', action='index', 
                                    packageId=1))
        # Test response...
        assert_in(['Package 1'], response)
