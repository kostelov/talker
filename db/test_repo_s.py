from pytest import raises
from .errors import *
from .models_s import User, Contacts
from .repository_s import Repository
from .config_db import *
import sqlalchemy


class TestRepository:

    def setup(self):
        # Создаем БД в памяти
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        # Создаем пользователей и сохраняем в БД
        u = User('Max', 'Максим Максимов')
        self.session.add(u)
        users = [User('Nat'), User('Ivan', 'Иван Петров'), User('Nick', 'Николай')]
        self.session.add_all(users)
        # Добавляем связи в таблицу Contacts
        rel = [Contacts(1, 2), Contacts(2, 1), Contacts(1, 3), Contacts(3, 1)]
        self.session.add_all(rel)

        self.repo = Repository(self.session)

    def test_add_user(self):
        with raises(sqlalchemy.exc.ArgumentError):
            self.repo.add_user('Test')
        assert self.repo.user_exist('Max')

    def test_user_exist(self):
        assert self.repo.user_exist('Max')
        assert self.repo.user_exist('Nat')
        assert not self.repo.user_exist('None')

    def test_get_user(self):
        # Результат будет <User('Max')>
        maxim = self.repo.get_user('Max')
        assert maxim.name == 'Max'
        non = self.repo.get_user('None')
        assert non is None

    def test_get_contacts(self):
        max_con = self.repo.get_contacts('Max')
        assert len(max_con) != 0

    def test_add_contact(self):
        self.repo.add_contact('Max', 'Nat')
        con = self.repo.get_contacts('Max')
        assert len(con) != 0
        with raises(UserDoesNotExist):
            self.repo.add_contact('Ivan', 'None')

    def test_del_contact(self):
        self.repo.del_contact('Nat', 'Max')
        con = self.repo.get_contacts('Nat')
        assert len(con) == 0
        with raises(UserDoesNotExist):
            self.repo.add_contact('Max', 'None')

    def teardown(self):
        # self.session.rollback()
        self.session.close()
