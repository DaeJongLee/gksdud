from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QToolTip
from tray_icon import TrayIcon
from hotkey_manager import HotkeyManager
from text_converter import TextConverter
from utils import Signals
import sys  

class LanguageSwitcher:
    def __init__(self, app):
        self.app = app
        self.signals = Signals()
        self.tray_icon = TrayIcon(app, self.exit_app)
        self.hotkey_manager = HotkeyManager(self.on_activate)
        self.text_converter = TextConverter(self.signals)
        
        self.signals.convert_signal.connect(self.text_converter.convert_text)
        self.signals.update_status_signal.connect(self.show_tooltip)
        
        QToolTip.setFont(QFont('SansSerif', 18))

    def on_activate(self):
        self.text_converter.handle_activation()

    def show_tooltip(self, message):
        self.text_converter.show_tooltip(message)

    def run(self):
        self.tray_icon.show()
        sys.exit(self.app.exec_())

    def exit_app(self):
        self.hotkey_manager.stop()
        self.app.quit()