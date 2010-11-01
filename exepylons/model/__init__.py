"""The application's model objects"""
from exepylons.model.meta import Session, metadata, Base
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
