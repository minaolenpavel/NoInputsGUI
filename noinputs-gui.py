import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import QStringListModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("mainwindow.ui", self)

        self.model = QStringListModel()
        self.model.setStringList(["item1", "item2"])
        self.listView.setModel(self.model)

    def button_clicked(self):
        print("Button clicked!")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())