import sys
import PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QDialog
from PyQt6 import uic
from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import devicemanager
from about_dialog import AboutDialog
from install_dialog import InstallDialog
import installer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.device_manager = devicemanager.DeviceManager()

        if not installer.is_installed():
            install_dialog = InstallDialog(self)
            if install_dialog.exec() == QDialog.accepted:
                installer.install()
            else:
                exit()

        uic.loadUi("mainwindow.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        self.menuAbout.triggered.connect(self.show_about_dialogue)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Status"])
        self.deviceTableView.setShowGrid(False)
        self.deviceTableView.verticalHeader().hide()
        self.deviceTableView.horizontalHeader().hide()
        self.deviceTableView.setAlternatingRowColors(True)
        self.deviceTableView.setModel(self.model)
        self.deviceTableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # deviceTableView appearance modifications
        self.deviceTableView.horizontalHeader().setStretchLastSection(False)  # last column doesn't stretch
        self.deviceTableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # first column stretches
        self.deviceTableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # status column resizes to content

        self.load_inputs()

        self.inhibitButton.clicked.connect(self.inhibit_selected_device)
        self.uninhibitButton.clicked.connect(self.unhibit_selected_device)

    def show_about_dialogue(self):
        dialog = AboutDialog(self)
        dialog.show()

    def load_inputs(self):
        devices_list = self.device_manager.devices
        for d in devices_list:
            name_item = QStandardItem(d.name)
            # Status column
            status_text = "Disabled" if d.get_inhibit() else "Enabled"
            status_item = QStandardItem(status_text)
            # Align status to right
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.model.appendRow([name_item, status_item])

    def inhibit_selected_device(self):
        selected_indexes = self.deviceTableView.selectionModel().selectedIndexes()
        if selected_indexes:
            listview_index = selected_indexes[0]
            index = listview_index.row()
            print(index)
            self.device_manager.inhibit_device(index)
            self.update_status(index)

    def unhibit_selected_device(self):
        selected_indexes = self.deviceTableView.selectionModel().selectedIndexes()
        if selected_indexes:
            listview_index = selected_indexes[0]
            index = listview_index.row()
            self.device_manager.uninhibit_device(index)
            self.update_status(index)

    def update_status(self, row:int):
        device = self.device_manager.devices[row]
        status = device.get_inhibit()
        status_item = self.model.item(row,1)
        if status:
            status_item.setText("Disabled")
        else:
            status_item.setText("Enabled")

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
sys.exit(app.exec())