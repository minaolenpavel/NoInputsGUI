import PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QHeaderView, QDialog
from PyQt6 import uic
from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import sys
from __version__ import __version__

class AboutDialog(QDialog):
    def __init__(self, parent =None):
        super().__init__(parent)
        uic.loadUi("about_dialog.ui", self)
        self.okBtn.clicked.connect(self.close)
        # Set size as fixed
        self.setFixedSize(self.width(), self.height())
        # Hide extend window button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        self.versionLabel.setText(f"Version : {__version__}")

        self.githubLabel.setText('<a href="https://github.com/minaolenpavel/NoInputsGUI">GitHub Repo</a>')
        self.githubLabel.setOpenExternalLinks(True)

        self.originalLabel.setText('<a href="https://gitlab.com/S410/noinputs">Original project</a>')
        self.originalLabel.setOpenExternalLinks(True)

