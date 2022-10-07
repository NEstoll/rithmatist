import socket as socketLib
import threading
from tkinter import N
from forbiddance import Forbiddance
from game import Game
from queue import Empty, Full, Queue

from line import Line
from vigor import Vigor
from warding import Warding

class Server:
    #server instance of the game
    #authoritative copy of the game
    #validates player commands (anti-cheat)
    #relays player inputs to all players
    #TODO maybe back end stuff (save replay, spectator, etc.)

    maxBytes = 12
    outputQueues = []
    def __init__(self) -> None:
        #instantiate variables
        self.player1Input = Queue()
        self.player1Output = Queue()
        Server.outputQueues.append(self.player1Output)
        self.player2Input = Queue()
        self.player2Output = Queue()
        Server.outputQueues.append(self.player2Output)

        #setup socket
        self.server_socket = socketLib.socket(socketLib.AF_INET, socketLib.SOCK_STREAM)
        

    
    def setup(self, host: str="localhost", port:int=33514) -> None:
        #listen for player connections
        self.server_socket.bind((host, port))
        self.server_socket.listen(3)
        print("server up and listening")

        #wait for players to connect
        player1 = self.server_socket.accept()
        print("player1 connected: ", player1)
        #TODO add verification/validation with player computers

        #use threads to parse the messages from players TODO allow arbitrary players
        t1in = threading.Thread(target=self.parseInput, args=(player1[0], self.player1Input))
        t1in.start()
        t1out = threading.Thread(target=self.sendOutput, args=(player1[0], self.player1Output))
        t1out.start()


        #player 2
        player2 = self.server_socket.accept()
        print("player2 connected: ", player2)
        t2in = threading.Thread(target=self.parseInput, args=(player2[0], self.player2Input))
        t2in.start()
        t2out = threading.Thread(target=self.sendOutput, args=(player2[0], self.player2Output))
        t2out.start()
        #start game
        self.startGame()

    def sendOutput(self, socket:socketLib.socket, output: Queue) -> None:
        while True:
            if not output.empty():
                print("sending line")
                try :
                    data = output.get()
                    sent = socket.send(data)
                    while sent != len(data):
                        sent = socket.send(data[sent:])
                    print("line sent", data, len(data))
                except Full:
                    print("q error")
                

    def parseInput(self, socket:socketLib.socket, input: Queue) -> None:
        data = b''
        msg = socket.recv(Server.maxBytes)
        print("data recieved", msg, len(msg))
        while not msg == b'':
            data = msg.join([data, b''])
            if len(data) >= Server.maxBytes:
                print("line recieved")
                try:
                    input.put(self.parseMessage(data[:Server.maxBytes]))
                    for q in Server.outputQueues:
                        q.put(data[:Server.maxBytes]) #TODO better error checking
                    data = data[Server.maxBytes:]
                except Full:
                    print("q error")
            msg = socket.recv(Server.maxBytes-len(data))
        raise RuntimeError("socket broke")

    def parseMessage(self, data:bytes) -> Line:
        #TODO check first bit for validating states
        match data[0]:
            case 1:
                return Vigor((int.from_bytes(data[1:2], "big"), int.from_bytes(data[3:4], "big")), (int.from_bytes(data[5:6], "big"), int.from_bytes(data[7:8], "big")))
            case 2:
                return Forbiddance((int.from_bytes(data[1:2], "big"), int.from_bytes(data[3:4], "big")), (int.from_bytes(data[5:6], "big"), int.from_bytes(data[7:8], "big")))
            case 3:
                return Warding((int.from_bytes(data[1:2], "big"), int.from_bytes(data[3:4], "big")), (int.from_bytes(data[5:8], "big")))
            case 4:
                #TODO add lines of creation
                #return Vigor((int.from_bytes(data[1:2], "big"), int.from_bytes(data[3:4], "big")), (int.from_bytes(data[5:6], "big"), int.from_bytes(data[7:8], "big")))
                pass
            case _:
                pass
        raise RuntimeError("invalid message")


    def startGame(self) -> None:
        game = Game()
        while game.isRunning():
            #check for console commands (maybe?) TODO

            #get player input (if any)
            while not self.player1Input.empty():
                try:
                    print("player 1: ", self.player1Input.get())
                except Empty:
                    print("queue access failed")
            while not self.player2Input.empty():
                try:
                    print("player 2: ", self.player2Input.get())
                except Empty:
                    print("queue access failed")

            #run game simulation
            game.update()
    



if __name__ == "__main__":
    server = Server()
    server.setup()