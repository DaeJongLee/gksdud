import threading
import subprocess
from PyQt5.QtWidgets import QToolTip
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from pynput import keyboard
import os
import sys
from AppKit import NSPasteboard, NSStringPboardType

class TextConverter:
    def __init__(self, signals):
        self.signals = signals
        self.keyboard_controller = keyboard.Controller()
        self.selected_text = None
        print(f"Current working directory: {os.getcwd()}")
        print(f"Location of this script: {os.path.dirname(os.path.abspath(__file__))}")

    def handle_activation(self):
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
        self.selected_text = self.paste_from_clipboard()
        if self.selected_text and not self.selected_text.isspace():
            preview = self.get_preview_conversion(self.selected_text)
            message = f"선택한 내용 --- {self.selected_text}\n바뀌게 될 내용 --- {preview}\n변환하시려면 단축키를 누르세요"
            self.signals.update_status_signal.emit(message)
        else:
            self.signals.update_status_signal.emit("선택된 텍스트가 없습니다")
            self.selected_text = None

    def get_preview_conversion(self, text):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'converter.py')
        print(f"Attempting to run converter script at: {script_path}")
        try:
            result = subprocess.run([sys.executable, script_path, text], capture_output=True, text=True, check=True)
            print(f"Conversion preview result: {result.stdout}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error in preview conversion: {e}")
            print(f"Error output: {e.stderr}")
            return f"변환 중 오류 발생: {e}"

    def convert_selected_text(self):
        if self.selected_text and not self.selected_text.isspace():
            self.signals.convert_signal.emit(self.selected_text)
        else:
            self.signals.update_status_signal.emit("변환할 텍스트가 없습니다")
            self.selected_text = None

    def convert_text(self, text):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'converter.py')
        print(f"Attempting to run converter script at: {script_path}")
        try:
            result = subprocess.run([sys.executable, script_path, text], capture_output=True, text=True, check=True)
            converted_text = result.stdout.strip()
            print(f"Conversion result: {converted_text}")

            if converted_text:
                self.copy_to_clipboard(converted_text)
                
                self.keyboard_controller.press(keyboard.Key.backspace)
                self.keyboard_controller.release(keyboard.Key.backspace)
                
                with self.keyboard_controller.pressed(keyboard.Key.cmd):
                    self.keyboard_controller.press('v')
                    self.keyboard_controller.release('v')
            else:
                self.signals.update_status_signal.emit("변환 실패")
        except subprocess.CalledProcessError as e:
            print(f"Error in text conversion: {e}")
            print(f"Error output: {e.stderr}")
            self.signals.update_status_signal.emit(f"변환 중 오류 발생: {e}")
        
        self.selected_text = None

    def show_tooltip(self, message):
        cursor = QCursor.pos()
        QToolTip.showText(cursor, message)
        QTimer.singleShot(3000, QToolTip.hideText)

    def copy_to_clipboard(self, text):
        pb = NSPasteboard.generalPasteboard()
        pb.clearContents()
        pb.setString_forType_(text, NSStringPboardType)

    def paste_from_clipboard(self):
        pb = NSPasteboard.generalPasteboard()
        return pb.stringForType_(NSStringPboardType)