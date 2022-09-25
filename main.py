from chat_room import ChatRoom
from participant import Participant


def main():
    name = input('Digite o nome do participante\n')
    participant = Participant(name)
    while True:
        option = input('Digite a opcao:\n1. Iniciar Sala\n2. Entrar em uma sala\n')

        port = int(input('Digite a porta do canal\n'))
        if option == '1':
            channel = input('Digite o nome do canal\n')
            max_participants = int(input('Digite o máximo de participantes do canal\n'))
            room = ChatRoom(channel, max_participants, participant, port)
            room.list_participants()
            room.init_chat()
        else:
            participant.join_chat(port)


if __name__ == '__main__':
    main()