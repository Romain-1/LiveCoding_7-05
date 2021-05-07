import pygame, random, threading, socket
from pygame.locals import *
from threading import Thread

WINDOW_SIZE = (800, 600)
HOST = '54.36.103.96'
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


pygame.init()

blackboard = pygame.Surface(WINDOW_SIZE)
#bb_lock = threading.Lock()

#color = (
#    random.randrange(0, 255),
#    random.randrange(0, 255),
#    random.randrange(0, 255)
#)
color = (255, 0, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def display_screen():
    window = pygame.display.set_mode(WINDOW_SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            px = Pixel(pos, color)
            s.send(px.tostring().encode())
 #           with bb_lock:
            blackboard.set_at(pos, color)
        window.blit(blackboard, (0, 0))
        pygame.display.flip()


def talk_with_server():
    while True:
        r = s.recv(BUFSIZE).decode()
        while r[-1] != '.':
            r += s.recv(BUFSIZE).decode()
        args = r.split('.')
        for arg in args[:-1]:
            px = Pixel()
            px.fromstring(arg)
            #with bb_lock:
            blackboard.set_at(px.position, px.color)

Thread(target=display_screen).start()
Thread(target=talk_with_server).start()
