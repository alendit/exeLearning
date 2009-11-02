import SimpleHTTPServer
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor

class ServerController:
    """
    Controlling the build in server
    """

    PORT = 8000

    def __init__(self):

        self.socket = None


    def startServing(self, path):

        resource = File(path)
        factory = Site(resource)
        self.socket = reactor.listenTCP(self.PORT, factory)
        
    @property
    def running(self):
        return (bool)(self.socket)

    
    def stopServing(self):
        self.socket.stopListening()
        self.socket = None

