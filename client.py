from queue import Empty, Full, Queue
import socket as socketLib
import threading

from forbiddance import Forbiddance
from game import Game
import lib
from line import Line
from vigor import Vigor
from warding import Warding

class Player:
    #server instance of the game
    #authoritative copy of the game
    #validates player commands (anti-cheat)
    #relays player inputs to all players
    #TODO maybe back end stuff (save replay, spectator, etc.)
    maxBytes:int = 12

    def __init__(self) -> None:
        #instantiate variables
        #lib.pygame.init()
        lib.pygame.display.set_mode((0, 0), lib.pygame.FULLSCREEN)
        self.game = Game()
        self.lineQueue = Queue()

        #setup socket
        self.server = socketLib.socket(socketLib.AF_INET, socketLib.SOCK_STREAM)
        self.connect()
        #create thread for networking
        tout = threading.Thread(target=self.sendLines)
        tout.start()
        tin = threading.Thread(target=self.parseInput, args=(self.server,))
        tin.start() #TODO start threads later

    def parseInput(self, socket:socketLib.socket) -> None:
        data = b''
        msg = socket.recv(Player.maxBytes)
        print("data recieved", msg, len(msg))
        while not msg == b'':
            data = msg.join([data, b''])
            if len(data) >= Player.maxBytes:
                print("line recieved", list(data[:Player.maxBytes]))
                self.game.objects.append(self.parseMessage(data[:Player.maxBytes]))
                data = data[Player.maxBytes:]
                print(self.game.objects)
            msg = socket.recv(Player.maxBytes-len(data))
        raise RuntimeError("socket broke")

    def parseMessage(self, data:bytes) -> Line:
        #TODO check first bit for validating states
        match data[0]:
            case 1:
                return Vigor((int.from_bytes(data[1:3], "big"), int.from_bytes(data[3:5], "big")), (int.from_bytes(data[5:7], "big"), int.from_bytes(data[7:9], "big")), True)
            case 2:
                return Forbiddance((int.from_bytes(data[1:3], "big"), int.from_bytes(data[3:5], "big")), (int.from_bytes(data[5:7], "big"), int.from_bytes(data[7:9], "big")))
            case 3:
                return Warding((int.from_bytes(data[1:3], "big"), int.from_bytes(data[3:5], "big")), (int.from_bytes(data[5:9], "big")))
            case 4:
                #TODO add lines of creation
                #return Vigor((int.from_bytes(data[1:2], "big"), int.from_bytes(data[3:4], "big")), (int.from_bytes(data[5:6], "big"), int.from_bytes(data[7:8], "big")))
                pass
            case _:
                pass
        raise RuntimeError("invalid message")    

    
    def connect(self, host: str="localhost", port:int=33514) -> None:
        #listen for player connections
        self.server.connect((host, port))
        print("connected to server")

    def run(self) -> None:
        start = None
        while self.game.isRunning():
            for evt in lib.pygame.event.get(): #todo, add event handling to seperate class/game class
                if evt.type == lib.pygame.quit:
                    lib.pygame.quit()
                    running = False
                    break
                elif evt.type == lib.pygame.MOUSEBUTTONDOWN:
                    #starting to draw a line
                    start = lib.screenToGame(lib.pygame.mouse.get_pos())
                elif evt.type == lib.pygame.MOUSEBUTTONUP and start != None:
                    #line drawn
                    line = Vigor(start, lib.screenToGame(lib.pygame.mouse.get_pos()))
                    start = None    
                    #send to server
                    self.lineQueue.put(line)
                    #also add to local game, but check for server confirmation TODO handle duplicates
                    #self.game.objects.append(line)
                elif evt.type == lib.pygame.MOUSEMOTION:
                    #draw line locally
                    pass
            self.game.update()
            self.game.draw(lib.display())

    def sendLines(self) -> None:
        while True:
            if not self.lineQueue.empty():
                try:
                    self.sendLine(self.lineQueue.get())
                except Empty:
                    print("q error")
                    pass

    def sendLine(self, line:Line) -> None:
        print(line.toBytes(), ":::", self.parseMessage(line.toBytes()))
        data = line.toBytes().ljust(Player.maxBytes, b'\x00')
        print(data, "::::", self.parseMessage(data))
        sent = 0
        while sent < len(data):
            sent += self.server.send(data[sent:])
        print("line sent", list(data))





if __name__ == "__main__":
    localPlayer = Player()
    localPlayer.run()