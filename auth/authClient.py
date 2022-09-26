from getpass import getpass
import json
import socket

class DefaultAuth:
    tpc: socket.socket
    def __init__(self) -> None:
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = ('localhost', 8000)
        self.tcp.connect(dest)
    def signup(self) -> int:
        response = {
            "type": "signup",
            "data" : {
                "email": "",
                "pwd": ""
            }
        }
        email = input("Insira seu e-mail: ")
        pwd = getpass("Insira sua senha: ")
        conf_pwd = getpass("Confirme sua senha: ")
        if conf_pwd == pwd:
            response["data"]["email"] = email
            response["data"]["pwd"] = pwd
            return self.send_message_to_server(response)
        else:
            raise Exception("Confirmação de senha inválida\n")

    def login(self) -> int:
        response = {
            "type": "login",
            "data" : {
                "email": "",
                "pwd": ""
            }
        }
        email = input("Insira seu e-mail: ")
        pwd = getpass("Insira sua senha: ")
        response["data"]["email"] = email
        response["data"]["pwd"] = pwd
        return self.send_message_to_server(response)

    def validate_token(self, token):
        response = {
            "type": "validate",
            "data" : {
                "token": token,
            }
        }
        self.send_message_to_server(response)

    def close_connection(self):
        self.tcp.close()

    def send_message_to_server(self, message):
        self.tcp.send(json.dumps(message).encode('utf-8'))
        msg_rec = self.tcp.recv(1024)
        msg_rec = json.loads(msg_rec)
        print(msg_rec)
        if msg_rec['data']['status'] == 0:
            return msg_rec['data']['token']
        else:
            raise Exception(msg_rec['data']['message'])
