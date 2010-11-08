"""The application's model objects"""
from exepylons.model.meta import Session, Base
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    print "Binding %s" % engine
    Session.configure(bind=engine)

class Package(Base):
    ''' Information about exe packages '''
    __tablename__ = 'packages'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title= sa.Column(sa.String)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Package('%s')>" % self.title
    
class WebUser(Base):
    '''A User accessing the app'''
    __tablename__ = 'users'
    
    login = sa.Column(sa.String, primary_key=True)
    pass_hash = sa.Column(sa.String)
    
    def __init__(self, login, pass_hash):
        self.login = login
        self.pass_hash = pass_hash  

    def __repr__(self):
        return "<User('%s')>" % self.login