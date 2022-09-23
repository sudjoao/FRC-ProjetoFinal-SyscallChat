class AdminFunctions:
    def __init__(self) -> None:
        pass

    def show_commands(self) -> int:
        print('1. Criar nova sala')
        print('2. Adicionar um usuário a uma sala')
        print('3. Remover um usuário de uma sala')
        print('4. Fechar')
        option = int(input('Escolha uma opção\n'))
        while(option < 0 or option >4):
            option = int(input('Escolha uma opção válida\n'))
        return option