from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
import sys
from client import User
from jim.config import *
from handler import GuiReceiver


class DialogWindow(QtWidgets.QDialog):

    login = pyqtSignal(str)

    def __init__(self, parent=None):
        # Подключаем файл интерфейса клиента
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('login.ui', self)
        self.pushButtonOk.clicked.connect(self.click_ok)
        self.pushButtonCancel.clicked.connect(self.reject)

    def click_ok(self):
        text = self.lineEditLogin.text()
        self.lineEditLogin.clear()
        self.login.emit(text)
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Подключаем файл интерфейса клиента
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('main.ui', self)
        self.client = None

    @pyqtSlot(str)
    def get_login(self, username):
        self.client = User(username)
        self.client.start()
        contacts = self.client.get_contacts()
        # Контакты выводим в список
        for contact in contacts:
            self.listWidgetContact.addItem(contact)

    def make_window(self, login_object):
        login_object.login.connect(self.get_login)

    @pyqtSlot(str)
    def update_chat(self, text):
        try:
            window.listWidgetChat.addItem(text)
        except Exception as e:
            print(e)


class AllButton:
    """ Общий класс кнопки для работы со списком контактов """
    def __init__(self):
        self.client = window.client
        print(self.client)

class ButtonAddContact(AllButton):
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
#
#
# class ButtonDelContact(AllButton):
#     def on_clicked(self):
#         try:
#             # Выбираем контакт
#             item = window.listWidgetContact.currentItem()
#             contact_name = item.text()
#             if contact_name:
#                 # Удаляем контакт
#                 result = self.client.del_contact(contact_name)
#                 if result[CODE] == ACCEPTED:
#                     print(result[MESSAGE])
#                     window.listWidgetContact.clear()
#                     contacts = self.client.get_contacts()
#                     # Повторно получаем контакты и выводим в список
#                     for contact in contacts:
#                         window.listWidgetContact.addItem(contact)
#                 else:
#                     print(result[MESSAGE])
#         except Exception as e:
#             print(e)
#
#
# class ButtonSend(AllButton):
#     def on_clicked(self):
#         text = window.plainTextEditMsg.toPlainText()
#         if text:
#             try:
#                 contact_name = window.listWidgetContact.currentItem().text()
#                 self.client.message_send(contact_name, text)
#                 window.plainTextEditMsg.clear()
#                 msg = '{} << {}'.format(text, self.client.login)
#                 window.listWidgetChat.addItem(msg)
#             except Exception as e:
#                 print(e)


# class ChatList:

# @pyqtSlot(str)
# def update_chat(text):
#     try:
#         window.listWidgetChat.addItem(text)
#     except Exception as e:
#         print(e)


if __name__ == '__main__':
    # login = 'Nick'
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    login_dialog = DialogWindow()
    # client = User(login)
    # client.start()
    # listener = GuiReceiver(window.client.sock, window.client.receiver_queue)
    # listener.gotData.connect(window.update_chat)
    # thread_gui = QThread()
    # listener.moveToThread(thread_gui)
    # thread_gui.started.connect(listener.pull)
    # thread_gui.start()
    # contacts = client.get_contacts()
    # # Контакты выводим в список
    # for contact in contacts:
    #     window.listWidgetContact.addItem(contact)
    btn_add = ButtonAddContact()
    # btn_del = ButtonDelContact()
    # btn_send = ButtonSend()
    # window.pushButtonAddContact.clicked.connect(btn_add.on_clicked)
    # window.pushButtonDelContact.clicked.connect(btn_del.on_clicked)
    # window.pushButtonSend.clicked.connect(btn_send.on_clicked)
    window.make_window(login_dialog)
    window.show()
    login_dialog.exec()
    sys.exit(app.exec_())
