from admin_functions import AdminFunctions
from chat_room import ChatRoom
from participant import Participant


def main():
    channels = []
    admin_functions = AdminFunctions()
    name = input('Digite o nome do participante\n')
    channel = input('Digite o nome do canal\n')
    max_participants = int(input('Digite o máximo de participantes do canal\n'))
    participant = Participant(name, channel)
    room = ChatRoom(channel, max_participants, participant)
    channels.append(room)
    room.list_participants()
    option = input('Digite a opcao:\n1. Iniciar Sala\n2. Entrar em uma sala\n')
    if option == '1':
        room.init_chat()
    else:
        participant.join_chat()
            

if __name__ == '__main__':
    main()