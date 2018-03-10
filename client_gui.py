from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
import sys
from datetime import datetime
from client import User
from jim.config import *
from handler import GuiReceiver
from history.history_config import HistoryTo

history = HistoryTo()

class DialogWindow(QtWidgets.QDialog):

    login = pyqtSignal(str)

    def __init__(self, parent=None):
        # Подключаем файл интерфейса окна авторизации
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('login.ui', self)
        self.pushButtonOk.clicked.connect(self.click_ok)
        self.pushButtonCancel.clicked.connect(self.click_cancel)

    def click_ok(self):
        # Забираем логин и закрываем окно авторизации
        text = self.lineEditLogin.text()
        if text:
            self.lineEditLogin.clear()
            self.login.emit(text)
            self.close()
        else:
            print('Укажите логин')

    def click_cancel(self):
        self.login.emit(None)
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        # Подключаем файл интерфейса клиента
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('main.ui', self)
        self.client = ''

    @pyqtSlot(str)
    def get_login(self, username):
        if username:
            self.client = User(username)
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
        login_object.login.connect(self.get_login)

    @pyqtSlot(str)
    def update_chat(self, text):
        try:
            self.listWidgetChat.addItem(text)
        except Exception as e:
            print(e)


class AllButton:
    """ Общий класс кнопки для работы со списком контактов """
    def __init__(self, window):
        self.window = window


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
                # Формируем имя для файла истории
                # self.history_file_name = 'inf_{}.his'.format(contact_name)
                msg = self.window.client.message_send(contact_name, text)
                self.window.plainTextEditMsg.clear()
                # nix_time.strftime('%X', nix_time.localtime()), self.window.client.login, text
                tm = datetime.fromtimestamp(msg[TIME]).strftime('%X')
                text = '{} {}:\n{}\n'.format(tm, msg[USER], msg[MESSAGE])
                self.window.listWidgetChat.addItem(text)
                self.add_to_history(msg)
                # full_name_history_file = os.path.join(HISTORY_FOLDERS_PATH, self.history_file_name)
                # with open(full_name_history_file, 'a', encoding='utf-8') as hfile:
                #     hfile.write(msg)
            except Exception as e:
                print(e)

    @history
    def add_to_history(self, msg):
        return msg

class ChatEvent:
    """ Действие при выборе другой даписи в списке контактов """
    def __init__(self, window):
        self.window = window

    def change_contact(self):
        self.window.listWidgetChat.clear()
        # contact_name = self.window.listWidgetContact.currentItem().text()


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
