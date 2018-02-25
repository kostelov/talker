class UserAlreadyExists(Exception):

    def __init__(self, username):
        self.name = username

    def __str__(self):
        return 'Пользователь {}, уже существует'.format(self.name)


class UserDoesNotExist(Exception):

    def __init__(self, username):
        self.name = username

    def __str__(self):
        return 'Пользователь с именем {}, не найден'.format(self.name)
