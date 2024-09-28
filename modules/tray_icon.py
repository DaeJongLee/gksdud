from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class TrayIcon(QSystemTrayIcon):
    def __init__(self, app, exit_callback, about_callback, usage_callback):
        super().__init__(QIcon("assets/icon.png"), app)
        self.app = app
        self.exit_callback = exit_callback
        self.about_callback = about_callback
        self.usage_callback = usage_callback
        self.create_menu()

    def create_menu(self):
        menu = QMenu()

        # Usage action
        usage_action = QAction("사용법", self.app)
        usage_action.triggered.connect(self.usage_callback)
        menu.addAction(usage_action)

        # About action
        about_action = QAction("gksdud 소개", self.app)
        about_action.triggered.connect(self.about_callback)
        menu.addAction(about_action)

        # Separator
        menu.addSeparator()

        # Exit action
        exit_action = QAction("종료", self.app)
        exit_action.triggered.connect(self.exit_callback)
        menu.addAction(exit_action)

        self.setContextMenu(menu)

        