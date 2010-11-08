import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from exepylons.lib.base import BaseController, render

from exepylons.model.meta import Session
from exepylons import model

log = logging.getLogger(__name__)

class MainController(BaseController):
    
    requires_auth = True
    
    def index(self):
        # q = model.Session.query(model.Packages)
        # c.packages = q.limit(5)
        c.packages = Session.query(model.Package).all()

        c.test = "This is a test Message!!!11ryo-n"
        return render('/main/main.mako')
    
    def signout(self):
        '''Displayed when user signed out'''
        return "You've been signed out"

    def _denest(self, data):
        '''Densting a associative array to a param dictionary. 
        Every parameter starts with params
        '''
        params = {}
        for param in data:
            if param.startswith('params['):
                # lose 'params['
                params[param[7:-1]] = data[param]
        return params
     
    @jsonify
    def handleAjax(self):
        funcName = request.params['name']
        params = self._denest(request.params)
        try:
            function = getattr(self, "_handle%s" % funcName)
            # The handle function should get exactly the same
            # params as it expects
            result = function(**params)
            print "got results"
            return result

        except AttributeError, e:
            print e
            raise e
            print "Function %s not found" % funcName
        


    def _handleCreateNew(self, title=None):
        '''Create new package and bind it to a global storage'''
        print "### Creating new package ###"
        newPackage = model.Package(title)
        Session.add(newPackage)
        if title is None:
            title = newPackage.id
            newPackage.title = title
        Session.commit()
        packageId = newPackage.id
        print "### Package ID %s" % packageId
        return {'newId' : packageId}

