from admin_functions import AdminFunctions
from chat_room import ChatRoom
from participant import Participant


def main():
    channels = []
    admin_functions = AdminFunctions()
    name = input('Digite o nome do participante\n')
    channel = input('Digite o nome do canal\n')
    max_participants = input('Digite o máximo de participantes do canal\n')
    participant = Participant(name, channel)
    room = ChatRoom(channel, max_participants, participant)
    channels.append(room)
    room.list_participants()
    while True:
        option = admin_functions.show_commands()
        if option == 0:
            break
        if option == 1:
            channel = input('Digite o nome da nova sala\n')
            max_participants = input('Digite o máximo de participantes da sala\n')
            new_room = ChatRoom(channel, max_participants, participant)
            channels.append(new_room)
            for channel in channels:
                channel.list_participants()
            

if __name__ == '__main__':
    main()