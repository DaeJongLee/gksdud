import sys
import json
import os
import subprocess
import threading
import io
from contextlib import redirect_stderr
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QToolTip, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTimer
from pynput import keyboard, mouse
import pyperclip

class Signals(QObject):
    convert_signal = pyqtSignal(str)
    update_status_signal = pyqtSignal(str)
    show_permission_error_signal = pyqtSignal(str)

class PermissionDialog(QMessageBox):
    def __init__(self, error_message="", parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Warning)
        self.setText("권한 안내")
        self.setInformativeText(
            f"오류 메시지: {error_message}\n\n"
            "이 애플리케이션이 제대로 작동하려면 '접근성' 및 '입력 모니터링' 권한이 필요합니다.\n\n"
            "다음 단계를 따라 권한을 부여해 주세요:\n"
            "1. 시스템 환경설정 > 개인 정보 보호 및 보안 > 개인정보 보호로 이동합니다.\n"
            "2. 왼쪽 목록에서 '접근성'을 선택합니다.\n"
            "3. 오른쪽 목록에서 Terminal.app 또는 iTerm.app을 찾아 체크박스를 선택합니다.\n"
            "   (앱을 실행한 터미널 애플리케이션을 선택하세요)\n"
            "4. 같은 방식으로 '입력 모니터링'에서도 동일한 앱에 권한을 부여합니다.\n"
            "5. 설정을 완료한 후 이 애플리케이션을 다시 실행해주세요.\n\n"
            "주의: 권한 부여 후 터미널 앱을 재시작해야 할 수 있습니다."
        )
        self.setWindowTitle("권한 필요")

        self.checkbox = QCheckBox("다시 보지 않기")
        self.setCheckBox(self.checkbox)

        self.addButton("닫기", QMessageBox.AcceptRole)

    def exec(self):
        result = super().exec()
        return result, self.checkbox.isChecked()

class LanguageSwitcher:
    def __init__(self):
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("assets/icon.png"), self.app)
        self.create_tray_icon()
        self.signals = Signals()
        self.signals.convert_signal.connect(self.convert_text)
        self.signals.update_status_signal.connect(self.show_tooltip)
        self.signals.show_permission_error_signal.connect(self.show_permission_error)
        self.selected_text = None
        
        QToolTip.setFont(QFont('Arial', 18))

        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()

        self.init_hotkey()

    def create_tray_icon(self):
        menu = QMenu()
        exit_action = QAction("Exit", self.app)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def init_hotkey(self):
        f = io.StringIO()
        with redirect_stderr(f):
            try:
                self.listener = keyboard.GlobalHotKeys({
                    '<ctrl>+<shift>+l': self.on_activate
                })
                self.listener.start()
            except Exception as e:
                error_message = str(e)
                self.signals.show_permission_error_signal.emit(error_message)
                return

        error_output = f.getvalue()
        if "This process is not trusted!" in error_output:
            self.signals.show_permission_error_signal.emit(error_output)

    def show_permission_error(self, error_message):
        if self.get_setting('show_permission_dialog', True):
            dialog = PermissionDialog(error_message)
            _, dont_show_again = dialog.exec()
            if dont_show_again:
                self.save_setting('show_permission_dialog', False)

    def get_setting(self, key, default=None):
        try:
            with open('assets/settings.json', 'r') as f:
                settings = json.load(f)
            return settings.get(key, default)
        except FileNotFoundError:
            return default

    def save_setting(self, key, value):
        try:
            with open('assets/settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}
        settings[key] = value
        with open('assets/settings.json', 'w') as f:
            json.dump(settings, f)

    def show_tooltip(self, message):
        cursor = QCursor.pos()
        QToolTip.showText(cursor, message)
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
            preview = self.get_preview_conversion(self.selected_text)
            message = f"선택한 내용 --- {self.selected_text}\n바뀌게 될 내용 --- {preview}\n변환하시려면 단축키를 누르세요"
            self.signals.update_status_signal.emit(message)
        else:
            self.signals.update_status_signal.emit("선택된 텍스트가 없습니다")
            self.selected_text = None

    def get_preview_conversion(self, text):
        result = subprocess.run(['python', 'converter.py', text], capture_output=True, text=True)
        return result.stdout.strip()

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
        else:
            self.signals.update_status_signal.emit("변환 실패")
        
        self.selected_text = None

    def run(self):
        self.tray_icon.show()
        sys.exit(self.app.exec())

    def exit_app(self):
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.app.quit()

def show_initial_permission_dialog():
    dialog = PermissionDialog()
    result, dont_show_again = dialog.exec()
    if dont_show_again:
        switcher = LanguageSwitcher()
        switcher.save_setting('show_permission_dialog', False)
    return result == QMessageBox.AcceptRole

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if show_initial_permission_dialog():
        switcher = LanguageSwitcher()
        switcher.run()
    else:
        sys.exit()