import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from hashlib import md5

from webhelpers.html import literal

from exepylons.lib.base import BaseController, render
from exepylons.model.meta import Session
from exepylons.model import WebUser

log = logging.getLogger(__name__)

class LoginController(BaseController):

    def index(self):
        
        return render('/login/login.mako')
    
    def submit(self):
        login = str(request.params['login'])
        pass_hash = md5(str(request.params['password'])).hexdigest()
        print login, pass_hash
        
        user = Session.query(WebUser).get(login)
        print user
        if user is None or user.pass_hash != pass_hash:
            print "User or pass not found"
            if 'wrong_login' in session:
                session['wrong_login'] += 1
            else:
                session['wrong_login'] = 0
            return redirect(url(controller='login', action='index'))
        
        session['user'] = login
        session.save()
        
        if session.has_key('path_before_login'):
            redirect(session['path_before_login'])
        else:
            
            return literal('<p>You have successfully logged in</p>')

    def logout(self):
        if session.has_key('user'):
            del session['user']