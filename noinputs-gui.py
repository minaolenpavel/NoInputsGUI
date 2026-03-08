import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import QStringListModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import noinputs
import devicemanager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.device_manager = devicemanager.DeviceManager()

        uic.loadUi("mainwindow.ui", self)

        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.load_inputs()

    def load_inputs(self):
        devices_list = self.device_manager.devices
        for d in devices_list:
            item = QStandardItem(d.name)
            self.model.appendRow(item)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())