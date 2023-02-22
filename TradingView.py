import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from functools import partial
from scripts.start_window import StartWindow
from scripts.base_window import BaseWindow

country = []
good_themes = [1, 4, 6, 8, 10, 11, 16]

a = []


# ПРИМЕНЕНИЕ НОВОЙ ТЕМЫ
def apply_theme(app1, obj='', country1=[]):
    global a
    if obj:
        name = obj.comboBox.currentText()
        them = []
        with open('side_files/settings.txt', 'r', encoding="utf8") as f:
            them = f.read().split('\n')
        theme1 = open('side_files/settings.txt', 'w', encoding="utf8")
        them = [name] + them[1:]
        theme1.write('\n'.join(them))
        theme1.close()
        country = country1
        obj.close()
        a = []
        a.append(BaseWindow(country + ['']))
        a[0].applay_theme.clicked.connect(partial(apply_theme, app1, a[0], country))
        a[0].applay_theme_2.clicked.connect(partial(apply_theme, app1, a[0], country))
        a[0].applay_theme_3.clicked.connect(partial(apply_theme, app1, a[0], country))
    theme1 = open('side_files/settings.txt', 'r', encoding="utf8")
    theme = theme1.read().split('\n')[0]
    theme1.close()
    if 'Рекомендуется' in theme:
        theme = theme[:-14]
    file = QFile(f"themes/{theme}.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app1.setStyleSheet(stream.readAll())


# СОЗДАНИЕ ГЛАВНОГО ОКНА
def init_win(m, app1):
    global a
    if m.country:
        m.close()
        a.append(BaseWindow(m.country + ['']))
        a[0].applay_theme.clicked.connect(partial(apply_theme, app1, a[0], m.country))
        a[0].applay_theme_2.clicked.connect(partial(apply_theme, app1, a[0], m.country))
        a[0].applay_theme_3.clicked.connect(partial(apply_theme, app1, a[0], m.country))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_theme(app)
    ex1 = StartWindow()
    ex1.nextBtn.clicked.connect(partial(init_win, ex1, app))
    ex1.show()
    sys.exit(app.exec())
