import socket
import select
import sys

class Participant:
    name: str
    chat_socket: socket.socket
    room_port: int

    def __init__(self, name: str) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def join_chat(self, room_port: int):
        self.chat_socket = socket.socket()
        self.chat_socket.connect(('localhost', room_port))
        while True:
            readers, _, _ = select.select([sys.stdin, self.chat_socket], [], [])
            for reader in readers:
                if reader is self.chat_socket:
                    print(self.chat_socket.recv(1000).decode('utf-8'))
                else:
                    msg = sys.stdin.readline()
                    sended_msg = f'{self.name}: {msg[:-1]}' 
                    self.chat_socket.send(sended_msg.encode('utf-8'))
