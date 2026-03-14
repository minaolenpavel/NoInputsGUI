from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys

class InstallDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi("install_dialog.ui", self)
        # Set size as fixed
        self.setFixedSize(self.width(), self.height())
        # Hide extend window button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        # Button mapping
        self.btnYesNo.accepted.connect(self.installation_accepted)
        self.btnYesNo.rejected.connect(self.installation_canceled)
    
    def installation_accepted(self):
        self.accept()
        
    def installation_canceled(self):
        self.reject()