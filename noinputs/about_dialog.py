import PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QDialog
from PyQt6 import uic
from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import os
from __version__ import version

class AboutDialog(QDialog):
    def __init__(self, parent =None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "about_dialog.ui")
        uic.loadUi(ui_path, self)
        self.okBtn.clicked.connect(self.close)
        # Set size as fixed
        self.setFixedSize(self.width(), self.height())
        # Hide extend window button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        self.versionLabel.setText(f"Version : {version}")

        self.githubLabel.setText('<a href="https://github.com/minaolenpavel/NoInputsGUI">GitHub Repo</a>')
        self.githubLabel.setOpenExternalLinks(True)

        self.originalLabel.setText('<a href="https://gitlab.com/S410/noinputs">Original project</a>')
        self.originalLabel.setOpenExternalLinks(True)

