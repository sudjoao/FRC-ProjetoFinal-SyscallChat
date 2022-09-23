from participant import Participant


class ChatRoom:
    name: str
    max_participants: int
    participants: list
    owner: Participant

    def __init__(self, name, max_participants, owner: Participant) -> None:
        self.name = name
        self.max_participants = max_participants
        self.participants = [owner]
        self.owner = owner
    
    def join_room(self, participant: Participant):
        if len(self.participants) < self.max_participants:
            self.participants.append(participant)
        else:
            print(f"Essa sala já possui {self.max_participants} participantes. Espere alguém sair ou tente entrar em outra sala.")

    def leave_room(self, participant: Participant):
        self.participants.remove(participant)
        print(f'Participante {participant.name} saiu da sala')

    def list_participants(self):
        print(f'---Sala {self.name}---')
        for i, participant in enumerate(self.participants):
            print(f'\tParticipante {i}: {participant.name}')
        print('\n\n')
