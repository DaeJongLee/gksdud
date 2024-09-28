from setuptools import setup

APP = ['main.py']
DATA_FILES = ['assets']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['PyQt5'],
    'excludes': ['tkinter', 'numpy', 'scipy'],  # 사용하지 않는 큰 패키지들 제외
    'iconfile': 'assets/icon.icns',  # 아이콘 파일이 있다면 경로를 지정하세요
}

setup(
    app=APP,
    name='gksdud',
    data_files=[('assets', DATA_FILES)],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)