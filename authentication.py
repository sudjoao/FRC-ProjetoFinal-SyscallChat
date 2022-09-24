import hashlib
import json

class DefaultAuth:
    credentials: dict

    def __init__(self, credentials: dict = {}) -> None:
        self.start(credentials)

    def start(self, credentials: dict = {}) -> None:
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

    def signup(self) -> int:
        print(f"signup credentials: {self.credentials}")
        email = input("Insira seu e-mail: ")
        pwd = input("Insira sua senha: ")
        conf_pwd = input("Confirme sua senha: ")
        if email not in self.credentials.keys():
            if conf_pwd == pwd:
                enc = conf_pwd.encode()
                hash1 = hashlib.md5(enc).hexdigest()
                self.credentials[email] = hash1
                print("Conta criada com sucesso!\n")
                return 0
            else:
                print("Confirmação de senha inválida\n")
                return -1
        else:
            print("Email já cadastrado!\n")
            return -2

    def login(self) -> int:
        email = input("Insira seu e-mail: ")
        pwd = input("Insira sua senha: ")
        auth = pwd.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        if(
            email in self.credentials.keys() and 
            auth_hash == self.credentials[email]
        ):
            print("Login realizado com sucesso!\n")
            return 0
        else:
            print("Login falhou!\n")
            return -1

if __name__ == '__main__':
    auth = DefaultAuth()
    auth.signup()
    auth.commit()
    auth.login()