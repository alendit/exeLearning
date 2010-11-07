from exepylons.model import Package
from exepylons.model.meta import Base, Session
from exepylons.tests import *

from nose.tools import *
from exepylons.tests.test_tools import *

class TestMainController(TestController):
    
    # Number of packages for testing
    _COUNT = 5

    def setUp(self):
        Session.remove()
        Base.metadata.create_all(bind=Session.bind)
        self._createpackages(self._COUNT)
        
    def tearDown(self):
        Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
        
    def _createpackages(self, count):
        for number in xrange(count):
            package = Package("Package %s" % number)
            Session.add(package)
        Session.commit()
            
    def test_basic_elements(self):
        response = self.app.get(url(controller='main', action='index'))
        # Test response...
        assert_in(["Main Page", "<input", "common.js"], response)
        
    def test_packages(self):
        '''tests if links to packages are here'''
        response = self.app.get(url(controller='main', action='index'))

        assert_in(("<p><a href='/package/index/%s'>Package %s" \
            % (num, num - 1) for num in xrange(1, self._COUNT + 1)),
                                response)