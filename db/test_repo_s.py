from pytest import raises
from .repository_s import Repository
from .config_db import *
from .errors import *
import sqlalchemy


class TestRepository:

    def setup(self):
        self.session = session
        # u1 = User('Max', 'Максим Максимов')
        # self.session.add(u1)
        # users = [User('Nat'), User('Ivan', 'Иван Петров')]
        # self.session.add_all(users)

        self.repo = Repository(self.session)

    def test_add_user(self):
        with raises(sqlalchemy.exc.ArgumentError):
            self.repo.add_user('Test')
        assert self.repo.user_exist('Test')

    def test_user_exist(self):
        assert self.repo.user_exist('Max')
        assert self.repo.user_exist('Nat')
        assert not self.repo.user_exist('None')

    def teardown(self):
        self.session.rollback()
