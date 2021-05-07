import socket

WINDOW_SIZE = (800, 800)
HOST = '0.0.0.0'
PORT = 1234

BUFSIZE = 2048

class Pixel(object):
    def __init__(self, position = (0, 0), color = (0, 0, 0)):
        self.position = position
        self.color = color

    def tostring(self):
        return f"{self.position[0]},{self.position[1]},{self.color[0]},{self.color[1]},{self.color[2]}."

    def fromstring(self, string):
        args = string.split(',')
        self.position = (int(args[0]),int(args[1]))
        self.color = (int(args[2]),int(args[3]),int(args[4]))
