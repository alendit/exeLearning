"""Setup the ExePylons application"""
import logging
import os

import pylons.test

from exepylons.config.environment import load_environment
from exepylons.model.meta import Session, Base
from exepylons.model import WebUser
from hashlib import md5

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup exepylons here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    
    # Deleting the old database
    Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    
    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)
    
    # Create admin if it's not a test
    if not pylons.test.pylonsapp:
        Session.add(WebUser('admin', md5('admin').hexdigest()))
        Session.commit()
    
