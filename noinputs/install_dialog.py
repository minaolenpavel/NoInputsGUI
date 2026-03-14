from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic
from PyQt6.QtCore import Qt
import os

class InstallDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "install_dialog.ui")
        uic.loadUi(ui_path, self)
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