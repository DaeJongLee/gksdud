import sys
from PyQt5.QtWidgets import QApplication
from modules.language_switcher import LanguageSwitcher
from modules.tray_icon import TrayIcon

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Set application information
    app.setApplicationName("gksdud")
    app.setApplicationVersion("1.0.1")
    app.setOrganizationName("daejonglee")
    app.setOrganizationDomain("https://github.com/daejonglee")

    # Create language switcher
    language_switcher = LanguageSwitcher(app)

    # Create tray icon
    tray_icon = TrayIcon(app,language_switcher.exit_app, language_switcher.about_gksdud, language_switcher.show_usage)

    # Run the application
    language_switcher.run()
    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()