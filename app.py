import sys
import subprocess
import threading
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QToolTip
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTimer
from pynput import keyboard, mouse
import pyperclip

class Signals(QObject):
    convert_signal = pyqtSignal(str)
    update_status_signal = pyqtSignal(str)

class LanguageSwitcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self.app)
        self.create_tray_icon()
        self.init_hotkey()
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()
        self.signals = Signals()
        self.signals.convert_signal.connect(self.convert_text)
        self.signals.update_status_signal.connect(self.show_tooltip)
        self.selected_text = None
        
        # 툴팁 폰트 설정
        QToolTip.setFont(QFont('SansSerif', 20))

    def create_tray_icon(self):
        menu = QMenu()
        exit_action = QAction("Exit", self.app)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def init_hotkey(self):
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+l': self.on_activate
        })
        self.listener.start()

    def show_tooltip(self, message):
        cursor = QCursor.pos()
        QToolTip.showText(cursor, message)
        # 3초 후에 툴팁을 숨기도록 타이머 설정
        QTimer.singleShot(3000, QToolTip.hideText)

    def on_activate(self):
        if self.selected_text is None:
            self.get_selected_text()
        else:
            self.convert_selected_text()

    def get_selected_text(self):
        with self.keyboard_controller.pressed(keyboard.Key.cmd):
            self.keyboard_controller.press('c')
            self.keyboard_controller.release('c')
        
        threading.Timer(0.2, self.process_clipboard).start()

    def process_clipboard(self):
        self.selected_text = pyperclip.paste()
        if self.selected_text and not self.selected_text.isspace():
            message = f"선택됨: [{self.selected_text}]\n변환하려면 Ctrl+Shift+L을 다시 누르세요"
            self.signals.update_status_signal.emit(message)
        else:
            self.signals.update_status_signal.emit("선택된 텍스트가 없습니다")
            self.selected_text = None

    def convert_selected_text(self):
        if self.selected_text and not self.selected_text.isspace():
            self.signals.convert_signal.emit(self.selected_text)
        else:
            self.signals.update_status_signal.emit("변환할 텍스트가 없습니다")
            self.selected_text = None

    def convert_text(self, text):
        result = subprocess.run(['python', 'converter.py', text], capture_output=True, text=True)
        converted_text = result.stdout.strip()

        if converted_text:
            pyperclip.copy(converted_text)
            
            self.keyboard_controller.press(keyboard.Key.backspace)
            self.keyboard_controller.release(keyboard.Key.backspace)
            
            with self.keyboard_controller.pressed(keyboard.Key.cmd):
                self.keyboard_controller.press('v')
                self.keyboard_controller.release('v')
            
            message = f"변환 완료: [{text}] -> [{converted_text}]"
            self.signals.update_status_signal.emit(message)
        else:
            self.signals.update_status_signal.emit("변환 실패")
        
        self.selected_text = None

    def run(self):
        self.tray_icon.show()
        sys.exit(self.app.exec_())

    def exit_app(self):
        self.listener.stop()
        self.app.quit()

if __name__ == "__main__":
    switcher = LanguageSwitcher()
    switcher.run()