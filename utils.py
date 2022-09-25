from communication import CommunicationProtocol
from data import Data


def get_message_from_json(json_msg) -> str:
    return f'{json_msg["data"]["user"]}: {json_msg["data"]["message"]}'

def get_formated_message(message, name, method):
    print(message)
    data = Data(name, message)
    communication_protocol = CommunicationProtocol(method, data)
    return f'{communication_protocol}'.encode('utf-8')