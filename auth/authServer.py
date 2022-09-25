import select
import socket
import sys
import hashlib
import json

from uuid import uuid4

class AuthServer:
    sock: socket.socket
    credentials: dict = {}
    valid_tokens: list = []
    inputs: list = []
    conn_map: dict = {}
    port: int = 8000

    def __init__(self, credentials: dict = {}) -> None:
        self.start(credentials)

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.bind(('localhost', self.port))
        self.sock.listen(100)
        self.inputs = [self.sock]
        while self.inputs:
            readers, _, _ = select.select(self.inputs, [], [])
            for reader in readers:
                if reader is self.sock:
                    self.connect_to_server(reader)
                elif isinstance(reader, socket.socket):
                    self.read_message(reader)


    def __del__(self) -> None:
        self.commit()
        for input in self.inputs:
            input.shutdown(socket.SHUT_RDWR)
            input.close()

    def read_message(self, reader: socket.socket):
        response = {
            "type": "response",
            "data" : {
                "status": -1,
                "message": "Json inválido",
                "token": ""
            }
        }
        msg = reader.recv(1024).decode('utf-8')
        if msg:
            print(f'{msg}')
            try:
                command = json.loads(msg)
                if command["type"] == "signup":
                    response = self.signup(
                        command["data"]["email"],
                        command["data"]["pwd"],
                    )
                elif command["type"] == "login":
                    response = self.login(
                        command["data"]["email"],
                        command["data"]["pwd"],
                    )
                elif command["type"] == "disconnect":
                    self.disconnect_from_server(
                        command["data"]["token"],
                        reader
                    )
                    response["data"]["status"] = 0
                    response["data"]["message"] = "Desconectado"
                elif command["type"] == "validate":
                    response["data"]["status"] = self.validate_token(
                        command["data"]["token"],
                    )
                else:
                    response["data"]["message"] = "Comando inválido"
                print(response)
                reader.send(json.dumps(response).encode('utf-8'))
            except:
                print(json.dumps(response).encode('utf-8'))
                reader.send(json.dumps(response).encode('utf-8'))

    def connect_to_server(self, reader: socket.socket):
        connection, address = reader.accept()
        connection.setblocking(0)
        self.conn_map[address] = connection
        self.inputs.append(connection)

    def disconnect_from_server(self, token: str, reader: socket.socket):
        conn = self.conn_map.pop(reader.getpeername())
        self.valid_tokens.remove(token)
        self.inputs.remove(conn)
        reader.shutdown()
        reader.close()

    def start(self, credentials: dict = {}) -> None:
        if credentials:
            print('wtf')
            try:
                with open("credentials.txt", "r") as f:
                    self.credentials = json.load(f)
                    self.credentials.update(credentials)
                    print(f"start credentials: {self.credentials}")
                f.close()
            except FileNotFoundError as error:
                print(
                    f"{error.strerror}\n" +
                    "Nenhuma credencial cadastrada até o momento.\n" +
                    "Arquivos de credenciais será criado."
                )
                with open('credentials.txt', 'w'): pass

    def commit(self) -> None:
        with open("credentials.txt", "w") as f:
            json.dump(self.credentials, f)
        f.close()

    def erase(self) -> None:
        self.credentials = {}
        with open('credentials.txt', 'w'): pass

    def signup(self, email: str, pwd: str) -> int:
        response = {
            "type": "response",
            "data" : {
                "status": -1,
                "message": "",
                "token": ""
            }
        }
        if email not in self.credentials.keys():
            enc = pwd.encode()
            hash1 = hashlib.md5(enc).hexdigest()
            self.credentials[email] = hash1
            response["data"]["status"] = 0
            response["data"]["message"] = "Conta criada com sucesso!"
            rand_token = uuid4()
            response["data"]["token"] = rand_token.hex
            self.valid_tokens.append(rand_token)
            return response
        else:
            response["data"]["status"] = -1
            response["data"]["message"] = "E-mail já cadastrado"
            return response

    def login(self, email: str, pwd: str) -> int:
        response = {
            "type": "response",
            "data" : {
                "status": -1,
                "message": "",
                "token": ""
            }
        }
        auth = pwd.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        if(
            email in self.credentials.keys() and
            auth_hash == self.credentials[email]
        ):
            response["data"]["status"] = 0
            response["data"]["message"] = "Login realizado com sucesso!"
            rand_token = uuid4()
            response["data"]["token"] = rand_token.hex
            self.valid_tokens.append(rand_token)
            return response
        else:
            response["data"]["status"] = -1
            response["data"]["message"] = "Login falhou!"
            return response

    def validate_token(self, token):
        return 0 if (token in self.valid_tokens) else -1