from PyQt5 import QtWidgets, uic
import sys
from client import User


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('main.ui', self)


class BtnConnect():
    def __init__(self, login):
        self.login = login

    def on_clicked(self):
        if window.pushButtonConnect.text() == 'Подключиться':
            self.client = User(self.login)
            self.client.start('w')
            self.contacts = self.client.get_contacts()
            for contact in self.contacts:
                window.listWidgetContactList.addItem(contact)
            window.pushButtonConnect.setText('Отключиться')
            window.labelStatus.setText('В сети')
        elif window.pushButtonConnect.text() == 'Отключиться':
            window.pushButtonConnect.setText('Подключиться')
            window.labelStatus.setText('Не в сети')
            window.listWidgetContactList.clear()
            self.client.stop()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    btn_connect = BtnConnect('Max')
    window.pushButtonConnect.clicked.connect(btn_connect.on_clicked)
    window.show()
    sys.exit(app.exec_())