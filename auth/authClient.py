from getpass import getpass
import json
import socket

class DefaultAuth:
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
            self.send_message_to_server(response)
            return 0
        else:
            print("Confirmação de senha inválida\n")
            return -1

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
        self.send_message_to_server(response)

    def send_message_to_server(self, message):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = ('localhost', 8000)
        tcp.connect(dest)
        tcp.send(json.dumps(message).encode('utf-8'))
        msg_rec = tcp.recv(1024)
        msg_rec = json.loads(msg_rec)
        tcp.close()
        if msg_rec['data']['status'] == 0:
            return msg_rec['data']['token']
        else:
            raise Exception(msg_rec['data']['message'])