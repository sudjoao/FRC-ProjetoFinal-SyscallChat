import json

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
        pwd = input("Insira sua senha: ")
        conf_pwd = input("Confirme sua senha: ")
        if conf_pwd == pwd:
            response["data"]["email"] = email
            response["data"]["pwd"] = pwd
            # comunicação com o authServer aqui
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
        pwd = input("Insira sua senha: ")
        response["data"]["email"] = email
        response["data"]["pwd"] = pwd
        # comunicação com o authServer aqui

    def disconnect(self) -> int:
        response = {
            "type": "disconnect",
            "data" : {
                "token": ""
            }
        }
        # comunicação com o authServer aqui
