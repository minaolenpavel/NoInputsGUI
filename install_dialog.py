from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys
from __version__ import __version__

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
        print("accepted")
        self.accept()

    def installation_canceled(self):
        print("refused")
        self.reject()

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = InstallDialog()
window.show()
sys.exit(app.exec())
