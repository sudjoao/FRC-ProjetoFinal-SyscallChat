import socket
import select
import sys
from communication import CommunicationProtocol

from data import Data

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
        self.send_join_message()
        while True:
            readers, _, _ = select.select([sys.stdin, self.chat_socket], [], [])
            for reader in readers:
                if reader is self.chat_socket:
                    print(self.chat_socket.recv(1000).decode('utf-8'))
                else:
                    msg = sys.stdin.readline()
                    self.send_message(msg[:-1])

    def send_join_message(self):
        data = Data(self.name, "")
        communication_protocol = CommunicationProtocol('join', data)
        self.chat_socket.send(f'{communication_protocol}'.encode('utf-8'))

    def send_message(self, message):
        data = Data(self.name, message)
        communication_protocol = CommunicationProtocol('send_message', data)
        self.chat_socket.send(f'{communication_protocol}'.encode('utf-8'))