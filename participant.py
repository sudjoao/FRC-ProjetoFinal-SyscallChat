import socket
import select
import sys

class Participant:
    name: str
    # connection: socket.socket
    channel: str

    def __init__(self, name, channel) -> None:
        self.name = name
        # self.connection = connection
        self.channel = channel
    
    def __str__(self) -> str:
        return f'<{self.channel}>{self.name}'
    
    def join_chat(self):
        self.chat_socket = socket.socket()
        self.chat_socket.connect(('localhost', 7890))
        while True:
            readers, _, _ = select.select([sys.stdin, self.chat_socket], [], [])
            for reader in readers:
                if reader is self.chat_socket:
                    print(self.chat_socket.recv(1000).decode('utf-8'))
                else:
                    msg = sys.stdin.readline()
                    sended_msg = f'{self.name}: {msg}' 
                    self.chat_socket.send(sended_msg.encode('utf-8'))
