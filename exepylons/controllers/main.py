import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from exepylons.lib.base import BaseController, render

from exepylons import model
from exepylons.model.package import packageList

log = logging.getLogger(__name__)

class MainController(BaseController):

    def index(self):
        # q = model.Session.query(model.Packages)
        # c.packages = q.limit(5)
        c.packages = model.Session.query(model.Package).all()

        c.test = "This is a test Message"
        return render('/main/main.mako')

    def _denest(self, data):
        '''Densting a associative array to a param dictionary. 
        Every parameter starts with params
        '''
        params = {}
        for param in data:
            if param.startswith('params['):
                # loose 'params['
                params[param[7:-1]] = data[param]
        return params
     
    @jsonify
    def handleAjax(self):
        funcName = request.params['name']
        params = self._denest(request.params)
        try:
            function = getattr(self, "_handle%s" % funcName)
            # The handle function should expect exactly the same params, as
            # js sends
            result = function(**params)
            return result

        except AttributeError, e:
            print "Function %s not found" % funcName
        

    def _handleTest(self, param):
        return packageList

    def _handleCreateNew(self, title):
        '''Create new package and bind it to a global storage'''
        newPackage = model.Package(title)
        model.Session.add(newPackage)
        model.Session.commit()
        return newPackage.id

