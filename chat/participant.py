import json
import socket
import select
import sys
from chat.communication import CommunicationProtocol

from chat.data import Data
from chat.utils import  get_formated_message, get_message_from_json

class Participant:
    name: str
    chat_socket: socket.socket
    room_port: int
    token: str

    def __init__(self, name: str, token: str) -> None:
        self.name = name
        self.token = token

    def __str__(self) -> str:
        return f'{self.name}'

    def join_chat(self, room_port: int):
        self.chat_socket = socket.socket()
        self.chat_socket.connect(('localhost', room_port))
        self.send_join_message()
        self.inputs = [sys.stdin, self.chat_socket]
        while self.inputs:
            readers, _, _ = select.select(self.inputs, [], [])
            for reader in readers:
                if reader is self.chat_socket:
                    json_msg = json.loads(self.chat_socket.recv(1000).decode('utf-8'))
                    print(get_message_from_json(json_msg))
                else:
                    msg = sys.stdin.readline()[:-1]
                    if msg[0] == "/":
                        print(f'comando {msg} inserido')
                        self.handle_command(msg)
                    else:
                        self.send_message(get_formated_message(msg, self.name, 'send_message'))

    def send_join_message(self):
        self.chat_socket.send(get_formated_message('', self.name, 'join'))

    def send_message(self, message):
        self.chat_socket.send(message)

    def handle_command(self, command):
        if command == '/leave':
            self.chat_socket.send(get_formated_message('', self.name, 'leave'))
            self.inputs = []
            self.chat_socket.close()
        elif command == '/list':
            self.chat_socket.send(get_formated_message('', self.name, 'list'))
        elif command == '/help':
            print('Esses são os comandos disponíveis:\n/help: mostra a lista de comandos disponíveis\n/leave: você sai do chat\n/list: mostra a lista de participantes no chat')
        else:
            print(f'{command} não é um comando válido')