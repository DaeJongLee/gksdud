from PyQt5.QtCore import QObject, pyqtSignal

class Signals(QObject):
    convert_signal = pyqtSignal(str)
    update_status_signal = pyqtSignal(str)