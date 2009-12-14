import SimpleHTTPServer
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor
import time

class ServerController:
    """
    Controlling the build in server
    """

    PORT = 8000

    def __init__(self):

        self.server = None


    def startServing(self, path):

        resource = File(path)
        factory = Site(resource)
        self.server = reactor.listenTCP(self.PORT, factory)
        
    @property
    def running(self):
        return (bool)(self.server)

    def test(contents):
        print "FUCK YEAH!"
    
    def stopServing(self):
        print "Stopping Serving"
        if self.server:
            deffered = self.server.stopListening()
            deffered.addCallback(self.test)
            reactor.run()

