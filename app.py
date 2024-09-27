import sys
import subprocess
import threading
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal
from pynput import keyboard
import pyperclip
import time

class Signals(QObject):
    convert_signal = pyqtSignal(str)

class LanguageSwitcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self.app)
        self.create_tray_icon()
        self.init_hotkey()
        self.is_selecting = False
        self.keyboard_controller = keyboard.Controller()
        self.signals = Signals()
        self.signals.convert_signal.connect(self.convert_text)

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

    def on_activate(self):
        if not self.is_selecting:
            self.select_block()
        else:
            self.convert_selected_text()
        self.is_selecting = not self.is_selecting

    def select_block(self):
        with self.keyboard_controller.pressed(keyboard.Key.shift, keyboard.Key.alt):
            self.keyboard_controller.press(keyboard.Key.left)
            self.keyboard_controller.release(keyboard.Key.left)
        print("블록이 선택되었습니다. 다시 단축키를 눌러 변환하세요.")

    def convert_selected_text(self):
        with self.keyboard_controller.pressed(keyboard.Key.cmd):
            self.keyboard_controller.press('c')
            self.keyboard_controller.release('c')
        
        # Use threading instead of QTimer
        threading.Timer(0.1, self.process_clipboard).start()

    def process_clipboard(self):
        text = pyperclip.paste()
        if text:
            self.signals.convert_signal.emit(text)
        else:
            print("선택된 텍스트가 없거나 복사에 실패했습니다.")

    def convert_text(self, text):
        result = subprocess.run(['python', 'converter.py', text], capture_output=True, text=True)
        converted_text = result.stdout.strip()

        if converted_text:
            pyperclip.copy(converted_text)
            
            with self.keyboard_controller.pressed(keyboard.Key.cmd):
                self.keyboard_controller.press('v')
                self.keyboard_controller.release('v')
            print(f"변환 완료: {text} -> {converted_text}")
        else:
            print("변환된 텍스트가 없습니다.")

    def run(self):
        self.tray_icon.show()
        sys.exit(self.app.exec_())

    def exit_app(self):
        self.listener.stop()
        self.app.quit()

if __name__ == "__main__":
    switcher = LanguageSwitcher()
    switcher.run()