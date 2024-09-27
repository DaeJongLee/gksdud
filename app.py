import sys
import subprocess
import threading
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from pynput import keyboard
import pyperclip

class Signals(QObject):
    convert_signal = pyqtSignal(str)
    update_status_signal = pyqtSignal(str)

class StatusWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; border-radius: 10px;")
        
        layout = QVBoxLayout()
        self.status_label = QLabel("대기 중 (Ctrl+Shift+L)")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.setGeometry(100, 100, 250, 50)  # 위치와 크기 설정
        self.show()

    def update_status(self, status):
        self.status_label.setText(status)

class LanguageSwitcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self.app)
        self.status_window = StatusWindow()
        self.create_tray_icon()
        self.init_hotkey()
        self.keyboard_controller = keyboard.Controller()
        self.signals = Signals()
        self.signals.convert_signal.connect(self.convert_text)
        self.signals.update_status_signal.connect(self.status_window.update_status)
        self.selected_text = None

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

    def update_status(self, status):
        self.signals.update_status_signal.emit(status)

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
            status = f"선택됨: [{self.selected_text}]\n(Ctrl+Shift+L로 변환)"
            print(f"현재 선택된 블록은 [{self.selected_text}] 입니다. 변환하시려면 한번 더 단축키를 입력해주세요.")
        else:
            status = "선택된 텍스트 없음\n(Ctrl+Shift+L)"
            print("선택된 텍스트가 없습니다. 텍스트를 선택한 후 다시 시도해주세요.")
            self.selected_text = None
        self.update_status(status)

    def convert_selected_text(self):
        if self.selected_text and not self.selected_text.isspace():
            self.signals.convert_signal.emit(self.selected_text)
        else:
            status = "변환할 텍스트 없음\n(Ctrl+Shift+L)"
            print("변환할 텍스트가 없습니다. 먼저 텍스트를 선택해주세요.")
            self.selected_text = None
            self.update_status(status)

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
            
            status = f"[{text}] ->\n[{converted_text}]\n(Ctrl+Shift+L)"
            print(f"변환 완료: {text} -> {converted_text}")
        else:
            status = "변환 실패\n(Ctrl+Shift+L)"
            print("변환된 텍스트가 없습니다.")
        
        self.selected_text = None
        self.update_status(status)

    def run(self):
        self.tray_icon.show()
        sys.exit(self.app.exec_())

    def exit_app(self):
        self.listener.stop()
        self.app.quit()

if __name__ == "__main__":
    switcher = LanguageSwitcher()
    switcher.run()