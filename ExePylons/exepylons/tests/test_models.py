from exepylons.model.meta import Session
from exepylons.model import WebUser
from nose.tools import *
from hashlib import md5

def test_admin_in_db():
    
    user = Session.query(WebUser).get('admin')
    assert_true(user is not None)