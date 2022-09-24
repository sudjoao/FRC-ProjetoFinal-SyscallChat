import select
from socket import socket
import sys
import json
from participant import Participant


class ChatRoom:
    name: str
    max_participants: int
    participants: list
    owner: Participant
    chat_socket: socket
    port: int

    def __init__(self, name, max_participants, owner: Participant) -> None:
        self.name = name
        self.max_participants = max_participants
        self.participants = [owner]
        self.owner = owner

    def init_chat(self):
        self.chat_socket = socket()
        self.chat_socket.bind(('localhost', 7890))
        self.chat_socket.listen(1)
        while True: 
            con, cliente = self.chat_socket.accept()
            print('Concetado por')
            while True:
                msg = con.recv(1024).decode('utf-8')
                if not msg: break
                print(f'{msg}')
            con.close()
    
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
