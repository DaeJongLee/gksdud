from pynput import keyboard

class HotkeyManager:
    def __init__(self, callback):
        self.callback = callback
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+l': self.callback
        })
        self.listener.start()

    def stop(self):
        self.listener.stop()