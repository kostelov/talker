from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSlot
import sys
from client import User
from jim.config import *
from handler import GuiReceiver


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Подключаем файл интерфейса клиента
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('main.ui', self)


class ButtonList:
    """ Общий класс кнопки для работы со списком контактов """
    def __init__(self):
        self.client = client


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


class ButtonSend:
    def on_clicked(self):
        text = window.plainTextEditMsg.toPlainText()
        if text:
            try:
                contact_name = window.listWidgetContact.currentItem().text()
                client.message_send(contact_name, text)
                msg = '{} << '.format(text)
                window.listWidgetChat.addItem(msg)
            except Exception as e:
                print(e)


# class ChatList:

@pyqtSlot(str)
def update_chat(text):
    try:
        window.listWidgetChat.addItem(text)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    login = 'Nick'
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    client = User(login)
    client.start()
    listener = GuiReceiver(client.sock, client.receiver_queue)
    # chat = ChatList()
    listener.gotData.connect(update_chat)
    thread_gui = QThread()
    listener.moveToThread(thread_gui)
    thread_gui.started.connect(listener.pull)
    thread_gui.start()
    contacts = client.get_contacts()
    # Контакты выводим в список
    for contact in contacts:
        window.listWidgetContact.addItem(contact)
    btn_add = ButtonAddContact()
    btn_del = ButtonDelContact()
    btn_send = ButtonSend()
    window.pushButtonAddContact.clicked.connect(btn_add.on_clicked)
    window.pushButtonDelContact.clicked.connect(btn_del.on_clicked)
    window.pushButtonSend.clicked.connect(btn_send.on_clicked)
     # TypeError: connect() failed between GuiReceiver.gotData[str] and update_chat()
    window.show()
    sys.exit(app.exec_())
