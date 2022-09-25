from auth.authClient import DefaultAuth
from chat.participant import Participant
from chat.chat_room import ChatRoom

def main():
    print('Bem vindo ao bate papo uol')
    auth = DefaultAuth()
    option = int(input('Digite 1 para se cadastrar ou 2 para entrar com uma conta já existente'))
    if option == 1:
        while True:
            try:
                token = auth.signup()
                break
            except Exception as e:
                print(e)
    else:
        while True:
            try:
                token = auth.login()
                break
            except Exception as e:
                print(e)
    name = input('Digite o nome do participante\n')
    participant = Participant(name, token)
    while True:
        option = input('Digite a opcao:\n1. Iniciar Sala\n2. Entrar em uma sala\n')

        port = int(input('Digite a porta do canal\n'))
        if option == '1':
            channel = input('Digite o nome do canal\n')
            max_participants = int(input('Digite o máximo de participantes do canal\n'))
            room = ChatRoom(channel, max_participants, participant, port)
            room.init_chat()
        else:
            participant.join_chat(port)


if __name__ == '__main__':
    main()