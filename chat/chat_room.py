import select
import socket
import sys
import json
from time import sleep
from chat.participant import Participant
from chat.utils import get_formated_message, get_message_from_json


class ChatRoom:
    name: str
    max_participants: int
    participants: list
    owner: Participant
    chat_socket: socket.socket
    port: int
    inputs: list

    def __init__(self, name: str, max_participants: int, owner: Participant, port: int) -> None:
        self.name = name
        self.max_participants = max_participants
        self.participants = [owner.name]
        self.owner = owner
        self.port = port

    def init_chat(self):
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_socket.setblocking(0)
        self.chat_socket.bind(('localhost', self.port))
        self.chat_socket.listen(self.max_participants)
        self.inputs = [sys.stdin, self.chat_socket]
        print('Sala iniciada com sucesso')
        self.show_instructions()
        while self.inputs:
            readers, _, _ = select.select(self.inputs, [], [])
            for reader in readers:
                if reader is self.chat_socket:
                    self.join_room(reader)
                elif isinstance(reader, socket.socket):
                    self.read_message(reader)
                else:
                    self.type_message(reader)

    def read_message(self, reader: socket.socket):
        msg = reader.recv(1024).decode('utf-8')
        if msg:
            json_msg = json.loads(msg)
            user = json_msg['data']['user']
            if json_msg['type'] == 'join':
                self.participants.append(user)
                inform_msg = f'{user} entrou na sala'
                print(inform_msg)
                self.send_message(get_formated_message(inform_msg, '', 'send_message'), reader)
            elif json_msg['type'] == 'send_message':
                self.send_message(msg.encode('utf-8'), reader)
                print(get_message_from_json(json_msg))
            elif json_msg['type'] == 'leave':
                self.leave_room(json_msg['data']['user'])
            elif json_msg['type'] == 'list':
                self.list_participants(reader)

    def type_message(self, reader: socket.socket):
        msg = sys.stdin.readline()[:-1]
        if msg[0] == "/":
            self.handle_commands(msg)
        else:
            self.send_message(get_formated_message(msg, self.owner.name, 'send_message'), reader)

    def send_message(self, msg:str, reader: socket.socket = None):
        for i, input in enumerate(self.inputs):
            if i  > 1 and reader != input:
                input.sendall(msg)

    def join_room(self, reader: socket.socket):
        connection, _ = reader.accept()
        if len(self.participants) < self.max_participants:
            connection.setblocking(0)
            self.inputs.append(connection)
            connection.send(get_formated_message(f'Você entrou na sala {self.name}', '', 'connect'))
        else:
            connection.send(get_formated_message(f'Essa sala já possui {self.max_participants} participantes. Espere alguém sair ou tente entrar em outra sala.', '', 'disconnect'))

    def leave_room(self, participant: str):
        index = self.participants.index(participant)
        if index:
            self.participants.remove(participant)
            del self.inputs[index+1]
            leave_message = f'Participante {participant} saiu da sala'
            print(leave_message)
            self.send_message(get_formated_message(leave_message, '', 'send_message'))

    def list_participants(self, reader: socket.socket = None):
        participant_list = f'---Sala {self.name} ({len(self.participants)}/{self.max_participants})---'
        for i, participant in enumerate(self.participants):
            participant_list += f'\\nParticipante {i+1}: {participant}\\n'
        if reader:
            reader.send(get_formated_message(participant_list, '', 'send_message'))
        else:
            print(participant_list.replace('\\n', '\n'))

    def show_instructions(self):
        print('Esses são os comandos disponíveis:\n/help: mostra a lista de comandos disponíveis\n/close: você fecha a sala de chat\n/list: mostra a lista de participantes no chat.\nAlém disso para enviar uma mensagem basta digitá-la normalmente e apertar enter para enviar')

    def handle_commands(self, command):
        if command == '/close':
            print('Fechando sala...')
            for i, input in enumerate(self.inputs):
                if i > 1:
                    input.send(get_formated_message('A sala foi fechada, logo você foi removido.', '', 'disconnect'))
            self.inputs = []
            sleep(1)
            self.chat_socket.close()

        elif command == '/list':
            self.list_participants()

        elif command == '/help':
            self.show_instructions()

        else:
            print(f'{command} não é um comando válido')
