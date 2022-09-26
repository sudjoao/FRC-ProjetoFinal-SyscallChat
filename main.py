from auth.authClient import DefaultAuth
from chat.participant import Participant
from chat.chat_room import ChatRoom

def main():
    print('Bem vindo ao bate papo uol')
    auth = DefaultAuth()
    while True:
        option = int(input('Digite 1 para se cadastrar ou 2 para entrar com uma conta já existente:\n'))
        if option == 1:
            try:
                token = auth.signup()
                break
            except Exception as e:
                print(e)
        elif option == 2:
            try:
                token = auth.login()
                break
            except Exception as e:
                print(e)
        else:
            print('Opção digitada é inválida')

    name = input('Digite o nome do participante\n')
    participant = Participant(name, token)
    while True:
        option = int(input('Digite a opcao:\n1. Iniciar Sala\n2. Entrar em uma sala:\n'))
        print(participant.token)
        auth.validate_token(participant.token)
        if option == 0:
            print('Desconectando conta...')
            auth.close_connection()
            break
        elif option > 0 and option < 3:
            port = int(input('Digite a porta do canal\n'))
            if option == 1:
                channel = input('Digite o nome do canal\n')
                max_participants = int(input('Digite o máximo de participantes do canal:\n'))
                room = ChatRoom(channel, max_participants, participant, port)
                room.init_chat()
            elif option == 2:
                participant.join_chat(port)
        else:
            print('Opção digitada é inválida')


if __name__ == '__main__':
    main()