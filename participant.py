import socket


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