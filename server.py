from ast import While
from http import server
import socket
import game

class Server:
    #server instance of the game
    #authoritative copy of the game
    #validates player commands (anti-cheat)
    #relays player inputs to all players
    #TODO maybe back end stuff (save replay, spectator, etc.)

    def __init__(self) -> None:
        #instantiate variables
        self.player1 = None
        self.player2 = None

        #setup socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    
    def setup(self, host: str="localhost", port:int=33514):
        #listen for player connections
        self.server_socket.bind((host, port))
        self.server_socket.listen(3)
        print("server up and listening")
        while True:
            self.player1 = self.server_socket.accept()
            print("player1 connected: ", self.player1)
            self.player2 = self.server_socket.accept()
            print("player2 connected: ", self.player2)

    def startGame(self, player1, player2):
        pass


if __name__ == "__main__":
    server = Server()
    server.setup()