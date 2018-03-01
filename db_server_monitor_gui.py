from PyQt5 import QtWidgets, uic
import sys
from db.models_s import session
from db.repository_s import Repository


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # Подключаем файл интерфейса сервера
        uic.loadUi('db_server_monitor.ui', self)

class ButtonConnect():
    def __init__(self, session):
        self.repo = Repository(session)

    def on_clicked(self):
        # Подключаемся к БД получаем список всех клиентов
        window.listWidgetClients.clear()
        if window.pushButtonConnect.text() == 'Подключиться':
            for client in self.repo.get_clients():
                window.listWidgetClients.addItem(str(client.name))
            window.pushButtonConnect.setText('Отключиться')
        elif window.pushButtonConnect.text() == 'Отключиться':
            self.repo.session.close()
            window.listWidgetClients.clear()
            window.pushButtonConnect.setText('Подключиться')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    btn_connect = ButtonConnect(session)
    window.pushButtonConnect.clicked.connect(btn_connect.on_clicked)
    window.show()
    sys.exit(app.exec_())
