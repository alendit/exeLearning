import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from exepylons.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PackageController(BaseController):

    def index(self, packageId):
        c.package_name = "Package %s" % packageId
        return render('/package/package.mako')
