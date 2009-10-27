import SimpleHTTPServer
from multiprocessing import Process
import SocketServer
import urllib
import os



class ServerController:
    """
    Controlling the build in server
    """

    PORT = 8000

    def __init__(self):

        self.Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.httpd = SocketServer.TCPServer(("", self.PORT), self.Handler)
        self.servProc = None


    def startServing(self, path):

        if not self.servProc:
            self.servProc = Process(target=serveForever, 
                                    args=(self.httpd, path))
            self.servProc.start()

    @property
    def running(self):
        return (bool)(self.servProc)

    
    def stopServing(self):

        if self.servProc:
            self.servProc.terminate()
            self.servProc = None

def serveForever(server, path):
    os.chdir(path)
    server.serve_forever()


