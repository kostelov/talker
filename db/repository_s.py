from .models_s import User, Contacts
from .errors import *


class Repository:
    """ Серверное хранилище """
    def __init__(self, session):
        self.session = session

    def add_user(self, username, info=None):
        """ Добавление нового пользователя """
        new_user = User(username, info)
        self.session.add(new_user)
        self.session.commit()

    def user_exist(self, username):
        """ Проверяем существует ли пользователь """
        result = self.session.query(User).filter(User.name == username).count() > 0
        return result

    def get_user(self, username):
        """ Получить пользователя по имени """
        user = self.session.query(User).filter(User.name == username).first()
        return user

    def add_contact(self, user_name, contact_name):
        """ Добавляем пользователя в список контактов """
        contact = self.get_user(contact_name)
        if contact:
            user = self.get_user(user_name)
            if user:
                # Добавляем пользователей в список контактов друг к другу
                new_relation = [Contacts(user_id=user.uid, contact_id=contact.uid),
                                Contacts(user_id=contact.uid, contact_id=user.uid)]
                self.session.add_all(new_relation)
                self.session.commit()
            else:
                raise UserDoesNotExist(user)
        else:
            raise UserDoesNotExist(contact)

    def get_contacts(self, username):
        user = self.get_user(username)
        result = []
        if user:
            contacts = self.session.query(Contacts).filter(Contacts.user_id == user.uid)
            for user_contact in contacts:
                contact = self.session.query(User).filter(User.uid == user_contact.contact_id).first()
                result.append(contact)
        return result

    def del_contact(self, user_name, contact_name):
        """ Удалить пользователя из списка контактов """
        contact = self.get_user(contact_name)
        if contact:
            user = self.get_user(user_name)
            if user:
                del_contact = self.session.query(Contacts).filter(
                    Contacts.user_id == user.uid).filter(Contacts.contact_id == contact.uid).first()
                self.session.delete(del_contact)
                self.session.commit()
            else:
                raise UserDoesNotExist(user)
        else:
            raise UserDoesNotExist(contact)
