class Data:
    user: str
    message: str

    def __init__(self, user: str, message: str) -> None:
        self.user = user
        self.message = message

    def __str__(self) -> str:
        return '"data": { "user": "' + self.user + f'", "message": "{self.message}"' + ' }'