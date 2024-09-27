import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from pynput import keyboard
import pyperclip

class LanguageSwitcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self.app)
        self.create_tray_icon()
        self.init_hotkey()
        self.is_selecting = False
        self.keyboard_controller = keyboard.Controller()

    def create_tray_icon(self):
        menu = QMenu()
        exit_action = QAction("Exit", self.app)
        exit_action.triggered.connect(self.exit_app)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def init_hotkey(self):
        self.listener = keyboard.GlobalHotKeys({
            '<cmd>+<shift>+x': self.on_activate
        })
        self.listener.start()

    def on_activate(self):
        if not self.is_selecting:
            self.select_block()
        else:
            self.convert_selected_text()
        self.is_selecting = not self.is_selecting

    def select_block(self):
        # 쉬프트+옵션+왼쪽 화살표를 눌러 블록 선택
        with self.keyboard_controller.pressed(keyboard.Key.shift, keyboard.Key.alt):
            self.keyboard_controller.press(keyboard.Key.left)
            self.keyboard_controller.release(keyboard.Key.left)
        print("블록이 선택되었습니다. 다시 단축키를 눌러 변환하세요.")

    def convert_selected_text(self):
        # 선택된 텍스트 복사
        with self.keyboard_controller.pressed(keyboard.Key.cmd):
            self.keyboard_controller.press('c')
            self.keyboard_controller.release('c')
        
        # 복사된 텍스트가 클립보드에 반영될 시간을 줍니다
        QTimer.singleShot(300, self.process_clipboard)

    def process_clipboard(self):
        # 클립보드에서 텍스트 가져오기
        text = pyperclip.paste()
        
        if text:
            # converter.py 실행
            result = subprocess.run(['python', 'converter.py', text], capture_output=True, text=True)
            converted_text = result.stdout.strip()

            if converted_text:
                pyperclip.copy(converted_text)
                
                # 붙여넣기 시뮬레이션
                with self.keyboard_controller.pressed(keyboard.Key.cmd):
                    self.keyboard_controller.press('v')
                    self.keyboard_controller.release('v')
                print(f"변환 완료: {text} -> {converted_text}")
            else:
                print("변환된 텍스트가 없습니다.")
        else:
            print("선택된 텍스트가 없거나 복사에 실패했습니다.")

    def run(self):
        self.tray_icon.show()
        sys.exit(self.app.exec_())

    def exit_app(self):
        self.listener.stop()
        self.app.quit()

if __name__ == "__main__":
    switcher = LanguageSwitcher()
    switcher.run()