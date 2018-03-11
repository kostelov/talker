from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal, Qt, QEvent
import sys
import os
from datetime import datetime
from client import User
from jim.config import *
from handler import GuiReceiver
from history.history_config import HistoryTo, HISTORY_FOLDER_PATH

history = HistoryTo()

class DialogWindow(QtWidgets.QDialog):
    """ Будем принимать сигнал от диалогового окна авторизации"""
    login = pyqtSignal(str)

    def __init__(self, parent=None):
        # Подключаем файл интерфейса окна авторизации
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('login.ui', self)
        self.pushButtonOk.clicked.connect(self.click_ok)
        self.pushButtonCancel.clicked.connect(self.click_cancel)

    def click_ok(self):
        # Забираем логин, ip-адрес, порт и закрываем окно авторизации
        text = self.lineEditLogin.text()
        host = self.lineEditHost.text()
        port = self.lineEditPort.text()
        data = '{} {} {}'.format(text, host, port)
        if text:
            self.lineEditLogin.clear()
            # Вызываем сигнал
            self.login.emit(data)
            self.close()
        else:
            print('Укажите логин')

    def click_cancel(self):
        data = '{} {} {}'.format(None, '127.0.0.1', 7777)
        self.login.emit(data)
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Подключаем файл интерфейса клиента
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('main.ui', self)
        self.client = ''

    @pyqtSlot(str)
    def get_login(self, data):
        username = data.split()[0]
        ip = data.split()[1]
        port = int(data.split()[2])
        if username:
            self.client = User(username, ip, port)
            self.client.start()
            self.setWindowTitle('Talker - {}'.format(username))
            # Получаем список контактов для авторизованного пользователя
            contacts = self.client.get_contacts()
            # Контакты выводим в список
            for contact in contacts:
                self.listWidgetContact.addItem(contact)
        else:
            self.close()
            sys.exit()

    def make_window(self, login_object):
        # Связываем объект окно авторизации с функцией основного окна
        login_object.login.connect(self.get_login)

    @pyqtSlot(str)
    def update_chat(self, text):
        try:
            self.listWidgetChat.addItem(text)
        except Exception as e:
            print(e)

    def keyPressEvent(self, e):
        # Отправка сообщения по нажатию Enter, но только когда MainWindow в фокусе
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            btn_send.on_clicked()


class AllButton:
    """ Общий класс кнопки для работы со списком контактов """
    def __init__(self, main_window):
        self.window = main_window


class ButtonAddContact(AllButton):
    """ Кнопка добавления контакта в список """
    def on_clicked(self):
        # Берем имя из поля ввода
        contact_name = self.window.lineEditContactName.text()
        if contact_name:
            # Проверяем, что поле не пустое, отправляем запрос
            result = self.window.client.add_contact(contact_name)
            if result[CODE] == ACCEPTED:
                print(result[MESSAGE])
                # Обновляем список контактов
                self.window.listWidgetContact.addItem(contact_name)
                self.window.lineEditContactName.clear()
            else:
                print(result[MESSAGE])
        else:
            print('Укажите имя контакта')


class ButtonDelContact(AllButton):
    """ Кнопка удаления контакта из списка """
    def on_clicked(self):
        try:
            # Выбираем контакт
            item = self.window.listWidgetContact.currentItem()
            contact_name = item.text()
            if contact_name:
                # Удаляем контакт
                result = self.window.client.del_contact(contact_name)
                if result[CODE] == ACCEPTED:
                    print(result[MESSAGE])
                    current_item = self.window.listWidgetContact.takeItem(self.window.listWidgetContact.row(item))
                    del current_item
                else:
                    print(result[MESSAGE])
        except Exception as e:
            print(e)


class ButtonSend(AllButton):
    """ Кнопка отправки сообщения """
    def on_clicked(self):
        text = self.window.plainTextEditMsg.toPlainText()
        if text:
            try:
                contact_name = self.window.listWidgetContact.currentItem().text()
                msg = self.window.client.message_send(contact_name, text)
                self.window.plainTextEditMsg.clear()
                # nix_time.strftime('%X', nix_time.localtime()), self.window.client.login, text)
                tm = datetime.fromtimestamp(msg[TIME]).strftime('%X')
                text = '{} {}: {}'.format(tm, msg[USER], msg[MESSAGE])
                self.window.listWidgetChat.addItem(text)
                self.add_to_history(msg)
            except Exception as e:
                print(e)

    @history
    def add_to_history(self, msg):
        return msg


class ChatEvent:
    """ Действие при выборе другой записи в списке контактов """
    def __init__(self, main_window):
        self.window = main_window

    def change_contact(self):
        """ При выборе контакта из списка, подгружаем историю переписки"""
        self.window.listWidgetChat.clear()
        contact_name = self.window.listWidgetContact.currentItem().text()
        history_file_name = 'inf_{}.his'.format(contact_name)
        full_name_history_file = os.path.join(HISTORY_FOLDER_PATH, history_file_name)
        # Получаем дату файла истории. Нет смысла использовать, т.к. дата меняется при перезаписи файла
        # current_file_date = datetime.fromtimestamp(os.path.getmtime(full_name_history_file)).date()
        # Проверяем существует ли файл истории
        if os.path.exists(full_name_history_file):
            # self.window.listWidgetChat.addItem(str(current_file_date))
            with open(full_name_history_file, 'r', encoding='utf-8') as hfile:
                for line in hfile:
                    self.window.listWidgetChat.addItem(line.rstrip())
        else:
            # Если файла истории нет, ничего не делать
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    login_dialog = DialogWindow()
    btn_add = ButtonAddContact(window)
    btn_del = ButtonDelContact(window)
    btn_send = ButtonSend(window)
    set_item = ChatEvent(window)
    window.listWidgetContact.currentItemChanged.connect(set_item.change_contact)
    window.pushButtonAddContact.clicked.connect(btn_add.on_clicked)
    window.pushButtonDelContact.clicked.connect(btn_del.on_clicked)
    window.pushButtonSend.clicked.connect(btn_send.on_clicked)
    window.make_window(login_dialog)
    window.show()
    login_dialog.exec()
    if window.client:
        listener = GuiReceiver(window.client.sock, window.client.receiver_queue)
        listener.gotData.connect(window.update_chat)
        thread_gui = QThread()
        listener.moveToThread(thread_gui)
        thread_gui.started.connect(listener.pull)
        thread_gui.start()
    sys.exit(app.exec_())
