from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QToolTip, QMessageBox
from modules.tray_icon import TrayIcon
from modules.hotkey_manager import HotkeyManager
from modules.text_converter import TextConverter
from modules.utils import Signals
import sys

class LanguageSwitcher:
    def __init__(self, app):
        self.app = app
        self.signals = Signals()
        self.tray_icon = TrayIcon(app, self.exit_app, self.about_gksdud, self.show_usage)
        self.hotkey_manager = HotkeyManager(self.on_activate)
        self.text_converter = TextConverter(self.signals)

        self.signals.convert_signal.connect(self.text_converter.convert_text)
        self.signals.update_status_signal.connect(self.text_converter.show_tooltip)
        
        QToolTip.setFont(QFont('Arial', 18))

    def on_activate(self):
        self.text_converter.handle_activation()

    def run(self):
        self.tray_icon.show()
        sys.exit(self.app.exec_())

    def about_gksdud(self):
        QMessageBox.about(None, "About gksdud", 
                          "gksdud is a Korean/English keyboard input converter.\n"
                          "Version: 1.0.1\n"
                          "Author: DAE JONG LEE\n"
                          "GITHUB: (https://github.com/daejonglee)")

    def show_usage(self):
        usage_text = """
        gksdud 사용법:
        0. 시스템 세팅에서 접근성, 입력모니터링 허용
        1. 변환하고 싶은 텍스트를 선택합니다.
        2. Ctrl + Shift + L을 누릅니다.
        3. 선택한 텍스트와 변환될 내용이 툴팁으로 표시됩니다.
        4. 변환을 원하면 다시 Ctrl + Shift + L을 누릅니다. 
        5. 선택한 텍스트가 변환되어 붙여넣어집니다.
        """
        QMessageBox.information(None, "사용법", usage_text)

    def exit_app(self):
        self.hotkey_manager.stop()
        self.app.quit()
        sys.exit(0)