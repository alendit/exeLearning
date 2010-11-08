from exepylons.tests import *
from exepylons.tests.test_tools import *
from nose.tools import *

class TestLoginController(TestController):

    def test_index(self):
        # 
        response = self.app.get(url(controller='login', action='index'))
        _assert_in(['Login', 'Password'], response)
        # Test response...

    def test_return_to_login_on_wrong_user(self):
        response = self.app.post(url(controller='login', action='submit'),
                    params={'login' : 'foo', 'password' : 'barr'})
        assert_false(response.session.has_key('user'))
        _assert_in(['/login/index',], response.location)
        
    def test_wrong_password(self):
        response = self.app.post(url(controller='login', action='submit'),
                    params={'login' : 'admin', 'password' : 'barr'})
        assert_false(response.session.has_key('user'))
        _assert_in(['/login/index',], response.location)
        
    def test_login_on_post(self):
        response = self.app.post(url(controller='login', action='submit'),
                    params={'login' : 'admin', 'password' : 'admin'})
        print response
        _assert_in(['successfully', 'logged in',], response)
        _assert_in(['user',], response.session)
        assert_equals('admin', response.session['user'])
        
    def test_logout(self):
        response = self.app.post(url(controller='login', action='logout'))
        assert_false(response.session.has_key('user'))