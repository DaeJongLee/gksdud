import subprocess
import sys
from PyQt5.QtWidgets import QMessageBox, QApplication

def is_accessibility_enabled():
    """Check if the application has accessibility and input monitoring permissions."""
    cmd = 'tccutil list | grep -E "Terminal|iTerm"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return 'accessibility' in result.stdout and 'input_monitoring' in result.stdout

def show_permission_dialog():
    """Show a dialog to guide the user through granting accessibility permission."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("접근성 및 입력 모니터링 권한이 필요합니다")
    msg.setInformativeText("이 애플리케이션이 제대로 작동하려면 '접근성' 및 '입력 모니터링' 권한이 필요합니다. "
                           "다음 단계를 따라 권한을 부여해 주세요:\n\n"
                           "1. 시스템 환경설정 > 개인 정보 보호 및 보안 > 개인정보 보호로 이동합니다.\n"
                           "2. 왼쪽 목록에서 '접근성'을 선택하고, 오른쪽에서 Terminal 또는 iTerm2를 찾아 체크박스를 선택합니다.\n"
                           "3. 같은 방식으로 '입력 모니터링'에서도 Terminal 또는 iTerm2에 권한을 부여합니다.\n"
                           "4. 변경사항을 적용한 후 이 애플리케이션을 다시 실행해주세요.\n\n"
                           "권한 설정을 완료하셨나요?")
    msg.setWindowTitle("권한 요청")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    
    result = msg.exec_()
    
    return result == QMessageBox.Yes

def ensure_accessibility_permission():
    """Ensure the application has necessary permissions."""
    if is_accessibility_enabled():
        return True  # 권한이 이미 설정되어 있으면 아무 메시지도 표시하지 않고 True 반환

    while not is_accessibility_enabled():
        if show_permission_dialog():
            print("권한 설정을 확인 중입니다...")
        else:
            print("권한이 거부되었습니다. 애플리케이션을 종료합니다.")
            return False

    print("필요한 권한이 모두 부여되었습니다.")
    return True

if __name__ == "__main__":
    if ensure_accessibility_permission():
        print("애플리케이션을 시작합니다.")
    else:
        sys.exit(1)