
import sys
from PyQt5.QtWidgets import QApplication
from modules.language_switcher import LanguageSwitcher

def main():
    app = QApplication(sys.argv)
    
    # Set application information
    app.setApplicationName("gksdud")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Your Organization")
    app.setOrganizationDomain("yourdomain.com")

    # Create and run the language switcher
    switcher = LanguageSwitcher(app)
    switcher.run()

if __name__ == "__main__":
    main()