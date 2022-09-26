# Projeto de pesquisa - Criando ambientes virtuais de conversação com uso system call select()

## Alunos

| Nome | Matrícula |
|------|-----------|
|Gabriel Davi Pereira da Silva| 17/0010341 |
|Iuri Severo de Souza| 17/0145514 |
|João Pedro José Santos da Silva Guedes| 17/0013910 |

## Tecnologias
* Python

### Instalando Python
#### Linux

Para instalar o python3 na sua máquina, basta executar os seguintes comandos:
```
sudo apt-get update
sudo apt-get install python3.6
```
#### Outros sistemas operacionais
Basta baixar o executável referente a seu sistema operacional no link abaixo:
[Python Install](https://www.python.org/downloads/)

## Como rodar
### Servidor de autenticação

Para rodar o servidor de autenticação, você deve acessar a pasta *auth/* e lá dentro executar o seguinte comando:
```
python3 main.py
```

### Chat
Para rodar o chat basta entrar na raiz do projeto e executar o seguinte comando:
```
python3 main.py
```

Para cada usuário é necessário instanciar um programa python de chat.

## Possíveis problemas
### Servidor de autenticação
#### Porta já em uso
Ao tentar subir o servidor de autenticação, caso você se depare com um erro de porta já em uso, você pode alterar a porta, nos arquivos **authClient.py** e **authServer.py**, para a da sua preferência.

## Requisitos
* A criação de salas virtuais de bate-papo com nome da sala e limite de parcipantes
* Listar parcipantes de uma determinada sala
* Permir ingresso de clientes, com um idenficador, em uma sala existente, de acordo com o limite admido para a sala
* Saída de clientes de uma sala em que estava parcipando
* Diálogo entre os clientes das salas