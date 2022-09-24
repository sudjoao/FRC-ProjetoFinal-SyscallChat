from data import Data


class CommunicationProtocol:
    type: str
    data: Data

    def __init__(self, type: str, data: Data) -> None:
        self.type = type
        self.data = data

    def __str__(self) -> str:
        return '{ "type": "' + self.type + '",' + f'{self.data}' + ' }'