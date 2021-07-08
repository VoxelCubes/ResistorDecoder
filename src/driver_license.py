import PySide6.QtWidgets as Qw

from ui_generated_files.ui_license import Ui_License



class LicenseAgreement(Qw.QDialog, Ui_License):
    """Displays license"""


    def __init__(self):
        Qw.QDialog.__init__(self)
        self.setupUi(self)
