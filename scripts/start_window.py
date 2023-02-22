from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from scripts import config
from functools import partial
from ui_files.start_window_ui import Ui_MainWindow as StartW
import sys


# КЛАСС СТАРТОВОГО ОКНА
class StartWindow(QMainWindow, StartW):
    def __init__(self):
        self.country = []
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icons/main.ico'))
        layout = QGridLayout()
        self.all_check_box = []
        self.setLayout(layout)
        self.bg = QButtonGroup()
        for i, k in enumerate(config.country[:-1]):
            self.b1 = QCheckBox(k)
            self.b1.setFont(QFont('Arial', 12))
            self.b1.setChecked(False)
            self.b1.toggled.connect(partial(self.btnstate, self.b1))
            self.checkBox.toggled.connect(partial(self.btnstate, 'ALL'))
            self.checkBox.setFont(QFont('Arial', 12))
            # layout.addWidget(self.b1, 0, i)

            list_widget_item = QListWidgetItem()
            list_widget_item.setSizeHint(self.b1.sizeHint())
            self.listWidget.addItem(list_widget_item)
            self.listWidget.setItemWidget(list_widget_item, self.b1)
            self.listWidget.scrollToItem(list_widget_item)
            self.all_check_box.append(self.b1)

        # self.nextBtn.clicked.connect(self.next_)
        self.nextBtn.setIcon(QIcon('logo.png'))
        self.nextBtn.setText('Дальше')

    def btnstate(self, btn):
        if self.sender() == self.checkBox and self.sender().isChecked():
            for i in range(len(self.all_check_box)):
                self.all_check_box[i].setChecked(True)
                self.country = config.country
        elif self.sender() != self.checkBox and btn.text() not in self.country:
            self.country.append(btn.text())
        elif self.sender() == self.checkBox and not self.sender().isChecked():
            for i in range(len(self.all_check_box)):
                self.all_check_box[i].setChecked(False)
                self.country = []
        elif self.sender() != self.checkBox and btn.text() in self.country\
                and not self.sender().isChecked():
            self.country.remove(btn.text())
