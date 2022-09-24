import select
import socket
import sys
import json
from participant import Participant


class ChatRoom:
    name: str
    max_participants: int
    participants: list
    owner: Participant
    chat_socket: socket.socket
    port: int

    def __init__(self, name: str, max_participants: int, owner: Participant, port: int) -> None:
        self.name = name
        self.max_participants = max_participants
        self.participants = [owner]
        self.owner = owner
        self.port = port

    def init_chat(self):
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_socket.setblocking(0)
        self.chat_socket.bind(('localhost', self.port))
        self.chat_socket.listen(self.max_participants)
        self.inputs = [sys.stdin, self.chat_socket]
        while self.inputs: 
            readers, _, _ = select.select(self.inputs, [], [])
            for reader in readers:
                if reader is self.chat_socket:
                    connection, _ = reader.accept()
                    connection.setblocking(0)
                    self.inputs.append(connection)
                elif isinstance(reader, socket.socket):
                    msg = reader.recv(1024).decode('utf-8')
                    if not msg: break
                    print(f'{msg}')
                    for i, input in enumerate(self.inputs):
                        if i  > 1 and reader != input:
                            input.sendall(msg.encode('utf-8'))
                else:
                    msg = sys.stdin.readline()
                    sended_msg = f'{self.owner.name}: {msg[:-1]}'
                    for i, input in enumerate(self.inputs):
                        if i  > 1 and reader != input:
                            input.sendall(sended_msg.encode('utf-8'))

        
    
    def join_room(self, participant: Participant):
        if len(self.participants) < self.max_participants:
            self.participants.append(participant)
        else:
            print(f"Essa sala já possui {self.max_participants} participantes. Espere alguém sair ou tente entrar em outra sala.")

    def leave_room(self, participant: Participant):
        self.participants.remove(participant)
        print(f'Participante {participant.name} saiu da sala')

    def list_participants(self):
        print(f'---Sala {self.name} ({len(self.participants)}/{self.max_participants})---')
        for i, participant in enumerate(self.participants):
            print(f'\tParticipante {i+1}: {participant.name}')
        print('\n\n')
