import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
import webbrowser
from scripts.news import get_news
from ui_files.stock_win_ui import Ui_MainWindow as StW
from functools import partial


# КЛАСС ОКНА С ДАННЫМИ АКЦИИ И НОВОСТЯМИ
class StockWindow(QMainWindow, StW):
    def __init__(self, data_lst):
        self.pixmap = None
        self.data_lst = data_lst
        super().__init__()
        self.setupUi(self)
        self.init_ui()

    # НАСТРОЙКА ДИЗАЙНА
    def init_ui(self):
        self.name_label.setText(str(self.data_lst[0]))
        self.logo.setText(str(self.data_lst[1]))
        self.price.setText(str(round(self.data_lst[5], 3)) + ' ')
        self.cur.setText(str(self.data_lst[6]))
        self.dinamic_val.setText(str(round(self.data_lst[3], 3)) + ' '
                                 + str(self.data_lst[6]) + '; ' + str(round(self.data_lst[2], 3)) + '%')
        self.turnover.setText(str(self.data_lst[4]))
        self.field.setText(str(self.data_lst[7]))
        self.country.setText(str(self.data_lst[8]))
        self.setWindowIcon(QIcon('icons/main.ico'))

        layout = QGridLayout()
        for i, data in enumerate(get_news(self.data_lst[9], self.data_lst[1], self.data_lst[-1])):
            s = ''
            for j in range(len(data[0])):
                if j % 30 == 0:
                    s += '\n'
                s += data[0][j]
            btn = QPushButton(s)
            btn.setMaximumSize(600, 140)
            btn.setMinimumSize(360, 140)
            btn.setFont(QFont('Times', 12))
            btn.clicked.connect(partial(webbrowser.open, f'https://ru.tradingview.com/news/{data[1]}/'))
            layout.addWidget(btn, i, 0)
        if self.data_lst[-1]:
            self.pixmap = QPixmap(f'icons/{self.data_lst[-1]}.svg')
            self.pixmap.fill(QtCore.Qt.transparent)
            w = self.pixmap.size().width()
            h = self.pixmap.size().height()

            clipPath = QtGui.QPainterPath()
            clipPath.addRoundedRect(QtCore.QRectF(0, 0, w, h), w // 2, h // 2)

            qp = QtGui.QPainter(self.pixmap)
            qp.setClipPath(clipPath)
            qp.drawPixmap(0, 0, QtGui.QPixmap(f'icons/{self.data_lst[-1]}.svg'))
            qp.end()
            self.icon.setPixmap(self.pixmap)

        w = QWidget()
        w.setLayout(layout)
        self.scrollArea.setWidget(w)
        self.scrollArea.setWidgetResizable(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = StockWindow([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ex1.show()
    sys.exit(app.exec())
