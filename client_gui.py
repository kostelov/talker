from PyQt5 import QtWidgets, uic
import sys
from client import User
from jim.config import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Подключаем файл интерфейса клиента
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('main.ui', self)


class ButtonList:
    """ Общий класс кнопки для работы со списком контактов """
    def __init__(self):
        self.client = client


class ButtonConnect(ButtonList):
    def on_clicked(self):
        # Подключаемся к серверу и получаем данные
        if window.pushButtonConnect.text() == 'Подключиться':
            self.client.start()
            contacts = self.client.get_contacts()
            # Контакты выводим в список
            for contact in contacts:
                window.listWidgetContact.addItem(contact)
            # Меняем состояние кнопок
            window.pushButtonConnect.setText('Отключиться')
            window.labelStatus.setText('В сети')
            window.pushButtonAddContact.setEnabled(True)
            window.pushButtonDelContact.setEnabled(True)
        elif window.pushButtonConnect.text() == 'Отключиться':
            # Меняем состояние кнопок, отключаемся, чистим список
            window.pushButtonConnect.setText('Подключиться')
            window.labelStatus.setText('Не в сети')
            window.pushButtonAddContact.setEnabled(False)
            window.pushButtonDelContact.setEnabled(False)
            window.listWidgetContact.clear()
            self.client.stop()


class ButtonAddContact(ButtonList):
    def on_clicked(self):
        # Берем имя из поля ввода
        contact_name = window.lineEditContactName.text()
        if contact_name:
            # Проверяем, что поле не пустое, отправляем запрос
            result = self.client.add_contact(contact_name)
            if result[CODE] == ACCEPTED:
                print(result[MESSAGE])
                # Обновляем список контактов
                window.listWidgetContact.addItem(contact_name)
                window.lineEditContactName.clear()
            else:
                print(result[MESSAGE])
        else:
            print('Укажите имя контакта')

class ButtonDelContact(ButtonList):
    def on_clicked(self):
        try:
            # Выбираем контакт
            item = window.listWidgetContact.currentItem()
            contact_name = item.text()
            if contact_name:
                # Удаляем контакт
                result = self.client.del_contact(contact_name)
                if result[CODE] == ACCEPTED:
                    print(result[MESSAGE])
                    window.listWidgetContact.clear()
                    contacts = self.client.get_contacts()
                    # Повторно получаем контакты и выводим в список
                    for contact in contacts:
                        window.listWidgetContact.addItem(contact)
                else:
                    print(result[MESSAGE])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    login = 'Nick'
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    client = User(login)
    btn_connect = ButtonConnect()
    btn_add = ButtonAddContact()
    btn_del = ButtonDelContact()
    window.pushButtonConnect.clicked.connect(btn_connect.on_clicked)
    window.pushButtonAddContact.setEnabled(False)
    window.pushButtonDelContact.setEnabled(False)
    window.pushButtonAddContact.clicked.connect(btn_add.on_clicked)
    window.pushButtonDelContact.clicked.connect(btn_del.on_clicked)
    window.show()
    sys.exit(app.exec_())
