from chat.communication import CommunicationProtocol
from chat.data import Data


def get_message_from_json(json_msg) -> str:
    returned_msg = json_msg["data"]["message"]
    if json_msg["data"]["user"] != '':
        returned_msg = f'{json_msg["data"]["user"]}: {json_msg["data"]["message"]}'
    return returned_msg

def get_formated_message(message, name, method):
    data = Data(name, message)
    communication_protocol = CommunicationProtocol(method, data)
    return f'{communication_protocol}'.encode('utf-8')