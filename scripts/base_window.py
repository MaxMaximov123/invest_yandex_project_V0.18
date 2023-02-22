import threading
import time
from datetime import datetime as dt
from functools import partial
from PyQt5 import QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtCore import QTimer
from scripts import config
from scripts.check_password import check_password
from scripts.db import DB
from scripts.investing import stoks
from scripts.notifiction import push
from scripts.stock_win import StockWindow
from ui_files.base_window_ui import Ui_MainWindow as BaseW
from ui_files.login_window_ui import Ui_MainWindow as LogW
import sys

# ДОПОЛНИТЕЛЬНЫЕ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
country = []
search_flag = True
all_data_stoks1 = {}
progress_bar_val = 0
progress_bar = None
all_stonks_from_investing = []


# ФУНКЦИЯ ДЛЯ ПРЕРЫВАНИЯ ПОТОКА
def sleep_qt(sec):
	loop = QEventLoop()
	QTimer.singleShot(sec, loop.quit())
	loop.exec()


# ПОЛУЧЕНИЕ ИНТЕРВАЛА ОБНОВЛЕНИЯ ПОРТФЕЛЯ
def get_case_min():
	with open('side_files/settings.txt', 'r', encoding="utf8") as f:
		data = f.read().split('\n')
	return float(data[1])


# ВОЗВРАЩАЕТ СОХРАНЕННЫЙ ЛОГИН И ПАРОЛЬ ИЗ ФАЙЛА saved_login.txt
def get_saved_login():
	with open('side_files/saved_login.txt') as file_with_login:
		file_text = file_with_login.read().split('\n')
		login = file_text[0].split(': ')[1]
		password = file_text[1].split(': ')[1]
		return login, password


# СОХРАНЕНИЕ ЛОГИНА И ПАРОЛЯ СЕССИИ В ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
LOGIN, PASSWORD = get_saved_login()
show_notifications_status = True


# ОБНОВЛЕНИЕ СОХРАНЕННОГО ЛОГИНА И ПАРОЛЯ
def update_saved_login(login, password):
	with open('side_files/saved_login.txt', 'w') as file_with_login:
		file_with_login.write(f'login: {login}\npassword: {password}')


# КЛАСС С ПОТОКАМИ ДЛЯ РЕАЛИЗАЦИИ PROGRESS BAR
class WorkThread(QThread):
	thread_signal = pyqtSignal(int)

	def __init__(self, parent, country1):
		super().__init__()
		self.country = country1
		self.parent = parent

	def run(self):
		global all_data_stoks1, search_flag, progress_bar_val, progress_bar, all_stonks_from_investing
		all_stonks_from_investing = []
		for i in range(len(self.country)):
			progress_bar_val = int(100 / len(self.country) * (i + 1))
			self.thread_signal.emit(progress_bar_val)
			all_stonks_from_investing.append(stoks(self.country[i]))


# КЛАСС ОКОШКА АУТЕНТИФИКАЦИИ
class LoginWin(QMainWindow, LogW):
	def __init__(self, btn1, btn2, tabWidget, for_acc_btn=False, for_acc_btn_2=False):
		super().__init__()
		self.tabWidget = tabWidget
		self.btn1 = btn1
		self.btn2 = btn2
		self.setupUi(self)
		self.setWindowIcon(QIcon('icons/main.ico'))
		self.login_btn.clicked.connect(self.login)
		self.register_btn.clicked.connect(self.register)
		self.show()
		self.for_acc_btn = for_acc_btn
		self.for_acc_btn_2 = for_acc_btn_2
		if self.for_acc_btn or for_acc_btn_2:
			self.login_lineEdit.setText(LOGIN)
			self.password_lineEdit.setText(PASSWORD)
		self.first_word = ''
		self.db = DB()

	# МЕТОД ДЛЯ ВХОДА В АККАУНТ
	def login(self):
		global LOGIN, PASSWORD
		login = self.login_lineEdit.text()
		password = self.password_lineEdit.text()
		if self.db.login_exists(login):
			if self.db.check_password(login, password):
				self.error_label.setText('Вы успешно авторизировались!')
				LOGIN, PASSWORD = login, password
				notif = threading.Thread(target=push, args=(
					'Статус аутентификации', f'Вы успешно авторизировались!', show_notifications_status))
				notif.start()
				self.db.add_notification(LOGIN, PASSWORD, 'Вы успешно авторизировались!', dt.now())
				self.tabWidget.setTabText(2, 'Уведомления🔔❗️')
				self.first_word = LOGIN[0]
				self.btn1.setText(self.first_word)
				self.btn2.setText(self.first_word)
				if self.save_login.isChecked():
					update_saved_login(login, password)
				else:
					update_saved_login('', '')
			else:
				self.error_label.setText('Неверный пароль!')
		else:
			self.error_label.setText('Этого логина не существует, можете его зарегистрировать')

	# МЕТОД ДЛЯ РЕГИСТРАЦИИ
	def register(self):
		global LOGIN, PASSWORD
		login = self.login_lineEdit.text()
		password = self.password_lineEdit.text()
		if not self.db.login_exists(login):
			status_check = check_password(password)
			if status_check == 'ok':
				self.error_label.setText('Вы успешно зарегистрировались!')
				LOGIN, PASSWORD = login, password
				notif = threading.Thread(target=push, args=(
					'Статус аутентификации', f'Вы успешно авторизировались!', show_notifications_status))
				notif.start()
				self.db.add_notification(LOGIN, PASSWORD, 'Вы успешно зарегистрировались!', dt.now())
				self.tabWidget.setTabText(2, 'Уведомления🔔❗️')
				self.first_word = LOGIN[0]
				self.btn1.setText(self.first_word)
				self.btn2.setText(self.first_word)
				self.db.add_stock(login, password, '', '')
				if self.save_login.isChecked():
					update_saved_login(login, password)
				else:
					update_saved_login('', '')
			else:
				self.error_label.setText(status_check)
				return
		else:
			self.error_label.setText('Этот логин занят, вы  можете попробывать войти')
			return


# КЛАСС С ОКНОМ PROGRESS BAR
class ProgressWin(QWidget):
	def __init__(self):
		super().__init__()
		self.pbar = QProgressBar(self)
		self.pbar.setGeometry(25, 30, 740, 40)
		self.setGeometry(600, 400, 800, 100)
		self.setWindowIcon(QIcon('icons/main.ico'))
		self.setWindowTitle("Загрузка")


# ПОЛУЧЕНИЕ ИНТЕРВАЛА ОБНОВЛЕНИЯ СПИСКА АКЦИЙ
def get_all_min():
	with open('side_files/settings.txt', 'r', encoding="utf8") as f:
		data = f.read().split('\n')
	return float(data[2])


#  КЛАСС С ГЛАВНЫМ ОКНОМ
class BaseWindow(QMainWindow, BaseW):
	# МЕТОД INIT
	def __init__(self, country1):
		super().__init__()
		self.thread_signal = None
		self.person_case_dict = None
		self.login_win = None
		self.person_case_matrix = None
		self.setupUi(self)
		self.thread = None
		self.date1 = None
		self.visual_k = None
		self.visual_k_up = None
		self.push = None
		self.stock_info_win = None
		self.new_notifications = None
		self.fill_notif_to_click = None
		self.show_notifications_status = None
		self.all_data_stoks = None
		self.base_stoks_matrix = None
		self.btn = None
		self.visual_matrix = None
		self.unification_stoks1 = None
		self.unification_stoks2 = None
		self.progress_bar = ProgressWin()
		self.progress_bar.show()
		self.db = DB()
		self.login, self.password = get_saved_login()
		self.country = country1
		self.update_btn_2.clicked.connect(self.generate)
		self.search_flag_for_table = True
		self.generate()
		self.person_case_ = []
		self.comboBox.addItems(config.themes)

	# МЕТОД ДЛЯ ВЫВОДА ЗНАЧЕНИЯ НА PROGRESS BAR
	def display_val(self):
		global progress_bar_val
		while search_flag:
			if progress_bar_val < 101:
				self.progress_bar.show()
				self.progress_bar.pbar.setValue(progress_bar_val)
				time.sleep(0.1)

	# МЕТОД, ВЫЗЫВАЮЩИЙСЯ ПРИ ОКОНЧАНИИ ЗАГРУЗКИ АКЦИЙ
	def on_thread_signal(self, value):
		global all_data_stoks1, search_flag
		self.progress_bar.pbar.setValue(value)
		if self.progress_bar.pbar.value() > 99:
			self.thread.terminate()
			self.thread.wait()
			all_stonks_dict = {}
			for i in all_stonks_from_investing:
				for key in i:
					all_stonks_dict[key] = all_stonks_dict.get(key, []) + i[key]
			all_data_stoks1 = all_stonks_dict
			search_flag = False
			self.progress_bar.close()
			if self.search_flag_for_table:
				self.init_ui()
				self.search_flag_for_table = False
			else:
				self.all_data_stoks = all_data_stoks1
				self.unification_stoks()
				self.tableWidget.setRowCount(len(self.all_data_stoks['name']))
				self.tableWidget.setColumnCount(len(self.all_data_stoks.keys()))
				self.base_stoks_matrix = [self.unification_stoks2[i] for i in sorted(self.unification_stoks2)]
				self.visual_matrix = self.base_stoks_matrix[:self.visual_k * 2]
				self.fill_table(self.visual_matrix)

	# ЗАПУСК ПОТОКА СО СБОРОМ ДАННЫХ
	def generate(self):
		if not self.search_flag_for_table:
			self.progress_bar = ProgressWin()
			self.progress_bar.show()
		self.progress_bar.pbar.setValue(1)
		self.thread = WorkThread(self, self.country)
		self.thread.thread_signal.connect(self.on_thread_signal)  # +++
		self.thread.start()

	# ИНИЦИАЛИЗАЦИЯ ОКНА ЛОГИН/ПАРОЛЬ
	def display_login_win(self):
		self.login_win = LoginWin(self.acc_btn, self.acc_btn_2, self.tabWidget, True, True)
		self.acc_btn.setText(LOGIN[0] if LOGIN else '')
		self.acc_btn_2.setText(LOGIN[0] if LOGIN else '')

	# МЕТОД С НАСТРОЙКОЙ ИНТЕРФЕЙСА, И ЗАПУСК ВСЕХ ОПЕРАЦИЙ
	def init_ui(self):
		global show_notifications_status
		# ПОБОЧНЫЕ ПЕРЕМЕННЫЕ
		self.date1 = []
		self.visual_k = 200
		self.visual_k_up = 0
		self.push = push
		self.new_notifications = False
		self.fill_notif_to_click = True
		self.show_notifications_status = True

		# ПОТОКИ ДЛЯ ОБНОВЛЕНИЯ ДАННЫХ
		timer = QTimer(self)
		timer.timeout.connect(self.person_case)
		timer.start(int(get_case_min() * 60 * 1000))

		timer1 = QTimer(self)
		timer1.timeout.connect(self.generate)
		timer1.start(int(get_all_min() * 60 * 1000))

		#  НАСТРОЙКИ
		self.applay_theme_2.clicked.connect(self.save_case_minut)
		self.applay_theme_3.clicked.connect(self.save_all_minut)
		self.doubleSpinBox.setValue(get_case_min())
		self.doubleSpinBox_2.setValue(get_all_min())
		self.checkBox.stateChanged.connect(self.show_notifications)
		with open('side_files/settings.txt', 'r', encoding="utf8") as f:
			them = f.read().split('\n')
		if them[0] in config.themes:
			self.comboBox.setCurrentIndex(config.themes.index(them[0]))
		if them[3] == 'True':
			self.checkBox.setChecked(True)
			self.show_notifications_status = True
			show_notifications_status = True
		else:
			self.checkBox.setChecked(False)
			self.show_notifications_status = False
			show_notifications_status = False
		self.setWindowIcon(QIcon('icons/main.ico'))

		# ДИЗАЙН КНОПОК
		self.search_bar.setStyleSheet("border-radius: 10px")
		self.update_btn.setIcon(QIcon('icons/restart.png'))
		self.update_btn_2.setIcon(QIcon('icons/restart.png'))
		self.pushButton.setIcon(QIcon('icons/restart.png'))

		# ОКНО ЛОГИН/ПАРОЛЬ
		self.acc_btn.clicked.connect(self.display_login_win)
		self.acc_btn.setText(LOGIN[0] if LOGIN else '')
		self.acc_btn_2.clicked.connect(self.display_login_win)
		self.acc_btn_2.setText(LOGIN[0] if LOGIN else '')

		# ПОИСК АКЦИЙ
		self.search_btn.clicked.connect(self.search_content)
		self.search_btn_2.clicked.connect(partial(self.search_content, True))
		self.update_btn.clicked.connect(self.person_case)
		self.update_btn.clicked.connect(self.check_account)

		# СБОР АКЦИЙ И ФОРМИРОВАНИЕ ГЛАВНОЙ ТАБЛИЦЫ
		self.all_data_stoks = all_data_stoks1
		self.unification_stoks()
		self.tableWidget.setRowCount(len(self.all_data_stoks['name']))
		self.tableWidget.setColumnCount(len(self.all_data_stoks.keys()))
		self.tableWidget_3.setColumnCount(4)
		self.base_stoks_matrix = [self.unification_stoks2[i] for i in sorted(self.unification_stoks2)]
		self.visual_matrix = self.base_stoks_matrix[:self.visual_k * 2]
		self.fill_table(self.visual_matrix)
		# self.tableWidget.resizeColumnsToContents()
		# self.tableWidget_3.resizeColumnsToContents()
		self.entered_row_column(2)

		# ОКНО УВЕДОМЛЕНИЙ
		self.fill_table_notif()
		self.pushButton.clicked.connect(self.check_account)
		self.pushButton.clicked.connect(self.fill_table_notif)
		self.clear_btn.clicked.connect(self.check_account)
		self.clear_btn.clicked.connect(self.del_all_notif)

		# НОСТРОЙКИ TABWIDGET
		self.tabWidget.installEventFilter(self)

		# ДАННЫЕ ПОРТФЕЛЯ
		self.person_case_matrix = []
		self.person_case()

		# РАЗМЕР ТЕКСТА В ПОЛЯХ
		self.tableWidget.setFont(QFont('Arial', config.WORD_SIZE_TABLE))
		self.tableWidget_2.setFont(QFont('Arial', config.WORD_SIZE_TABLE))
		self.tableWidget_3.setFont(QFont('Arial', config.WORD_SIZE_TABLE))

		# ОТОБРАЖЕНИЕ ОКНА
		self.showMaximized()

	# МЕТОД, ПОКАЗЫВАЮЩИЙ УВЕДОМЛЕНИЯ
	def show_notifications(self):
		global show_notifications_status
		status = str(self.checkBox.isChecked())
		with open('side_files/settings.txt', 'r', encoding="utf8") as f:
			data = f.read().split('\n')
		theme1 = open('side_files/settings.txt', 'w', encoding="utf8")
		data[3] = status
		theme1.write('\n'.join(data))
		theme1.close()
		if status == 'True':
			self.checkBox.setChecked(True)
			self.show_notifications_status = True
			show_notifications_status = True
		else:
			self.checkBox.setChecked(False)
			self.show_notifications_status = False
			show_notifications_status = False

	# ВОЗВРАЩАЕТ ИНТЕРВАЛ ОБНОВЛЕНИЯ ПОРТФЕЛЯ
	def save_case_minut(self):
		minut = self.doubleSpinBox.value()
		with open('side_files/settings.txt', 'r', encoding="utf8") as f:
			data = f.read().split('\n')
		theme1 = open('side_files/settings.txt', 'w', encoding="utf8")
		data[1] = str(minut)
		theme1.write('\n'.join(data))
		theme1.close()

	# ПРОВЕРЯЕТ НАЛИЧИЕ ПОЛЬЗОВАТЕЛЯ В БД
	def check_account(self):
		if not (LOGIN and PASSWORD and self.db.login_exists(LOGIN)):
			self.login_win = LoginWin(self.acc_btn, self.acc_btn_2, self.tabWidget)
			self.acc_btn.setText(LOGIN[0] if LOGIN else '')
			self.acc_btn_2.setText(LOGIN[0] if LOGIN else '')
			return False
		return True

	# ОЧИСТКА ТАБЛИЦЫ С УВЕДОМЛЕНИИЯМИ
	def del_all_notif(self):
		if self.check_account():
			dlg = QMessageBox(self)
			dlg.setWindowTitle("Подтверждение очистки")
			dlg.setFont(QFont('Arial', config.WORD_SIZE_TABLE - 2))
			dlg.setText("Вы уверены, что хотите удалить все уведомления?")
			dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			dlg.setIcon(QMessageBox.Question)
			button = dlg.exec()

			if button == QMessageBox.Yes:
				self.db.delete_all_notification(LOGIN)
				self.fill_table_notif()

	# ОБНОВЛЕНИЕ ИНТЕРВАЛА ОБНОВЛЕНИЯ ДАННЫХ АКЦИЙ
	def save_all_minut(self):
		minut = self.doubleSpinBox_2.value()
		with open('side_files/side_files/settings.txt', 'r', encoding="utf8") as f:
			data = f.read().split('\n')
		theme1 = open('side_files/settings.txt', 'w', encoding="utf8")
		data[2] = str(minut)
		theme1.write('\n'.join(data))
		theme1.close()

	# МЕТОД ДЛЯ ДОБАВЛЕНИЯ/УДАЛЕНИЯ АКЦИИ В ПОРТФЕЛЬ
	def add_stonk(self, stonk_name, country1):
		if self.sender().text() == '✅':
			if LOGIN and PASSWORD and self.db.login_exists(LOGIN):
				stonks_list = [i[0] for i in self.db.get_case(LOGIN)]
				if stonk_name not in stonks_list:
					self.db.add_stock(LOGIN, PASSWORD, stonk_name, country1)
					notif = threading.Thread(target=self.push, args=(
						'Статус акции', f'Акция "{stonk_name.strip()}" ДОБАВЛЕНА!',
						self.show_notifications_status))
					notif.start()
					self.db.add_notification(LOGIN, PASSWORD, f'Акция "{stonk_name.strip()}" ДОБАВЛЕНА!', dt.now())
					self.new_notifications = True
					self.tabWidget.setTabText(2, 'Уведомления🔔❗️')
				self.sender().setText('❌')
			else:
				self.login_win = LoginWin(self.acc_btn, self.acc_btn_2, self.tabWidget)
				self.acc_btn.setText(LOGIN[0] if LOGIN else '')
				self.acc_btn_2.setText(LOGIN[0] if LOGIN else '')
		elif self.sender().text() == '❌':  # Добавить уведомления
			if LOGIN and PASSWORD and self.db.login_exists(LOGIN):
				stonks_list = [i[0] for i in self.db.get_case(LOGIN)]
				if stonk_name in stonks_list:
					self.db.delete_stonk(self.login, stonk_name)
					notif = threading.Thread(target=self.push, args=(
						'Статус акции', f'Акция "{stonk_name.strip()}" УДАЛЕНА!',
						self.show_notifications_status))
					notif.start()
					self.db.add_notification(LOGIN, PASSWORD, f'Акция "{stonk_name.strip()}" УДАЛЕНА!', dt.now())
					self.new_notifications = True
					self.tabWidget.setTabText(2, 'Уведомления🔔❗️')
				self.sender().setText('✅')
			else:
				self.login_win = LoginWin(self.acc_btn, self.acc_btn_2, self.tabWidget)
				self.acc_btn.setText(LOGIN[0] if LOGIN else '')
				self.acc_btn_2.setText(LOGIN[0] if LOGIN else '')

	# ОТКРЫТИЕ ОКНА С ДАННЫМИ ПО АКЦИИ И НОВОСТЯМИ
	def stock_info(self, r, col):
		if col in [0, 1]:
			item = self.sender().item
			lst = [2, 3, 5]
			value = [float(item(r, c).text()) if c in lst else item(r, c).text().strip() for c in range(10)]
			if item(r, 0).text() in self.unification_stoks2:
				value.append(self.unification_stoks2[item(r, 0).text()][-1])
			else:
				for i in self.person_case_matrix:
					if item(r, 0).text() == i[0]:
						value.append(i[-1])
			self.stock_info_win = StockWindow(value)
			self.stock_info_win.show()

	# ФИЛЬТР СОБЫТИЙ
	def eventFilter(self, source, event):
		if self.tabWidget.currentIndex() == 2:
			self.new_notifications = False
			self.tabWidget.setTabText(2, 'Уведомления🔔')
			if self.fill_notif_to_click:
				self.fill_table_notif()
				self.fill_notif_to_click = False
		else:
			self.fill_notif_to_click = True
		return super(BaseWindow, self).eventFilter(source, event)

	# МЕТОД ДЛЯ ДИНАМИЧЕСКОЙ ПОДГРУЗКИ ТАБЛИЦЫ С АКЦИЯМИ
	def entered_row_column(self, r):
		r1 = self.visual_k - 25 if r >= self.visual_k else 0
		if len(self.visual_matrix) - r < 25 and len(self.visual_matrix) < len(self.base_stoks_matrix):
			self.visual_k_up = r1
			self.visual_matrix = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']] * r1 + self.base_stoks_matrix[
																						r1:r + self.visual_k]
			self.fill_table(self.visual_matrix)
		elif r - self.visual_k_up < 25 and self.visual_k_up > 24:
			self.visual_k_up = r1
			self.visual_matrix = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']] * r1 + self.base_stoks_matrix[
																						r1:r + self.visual_k]
			self.fill_table(self.visual_matrix)

	# ФОРМИРОВАНИЯ ТАБЛИЦЫ С ПОРТФЕЛЕМ ПОЛЬЗОВАТЕЛЯ
	def person_case(self):
		if self.db.login_exists(LOGIN) and self.db.check_password(LOGIN, PASSWORD):
			self.person_case_ = self.db.get_case(LOGIN)
			self.person_case_dict = {}
			for i in self.person_case_:
				self.person_case_dict[i[1].strip()] = self.person_case_dict.get(i[1].strip(), []) + [i[0]]
			self.person_case_matrix = []
			for key in self.person_case_dict:
				if key in self.country:
					for j in self.person_case_dict[key]:
						if j in self.unification_stoks2:
							self.person_case_matrix.append(self.unification_stoks2[j])
				else:
					stoks1 = stoks(key)
					for j in self.person_case_dict[key]:
						if j in stoks1['name']:
							index = stoks1['name'].index(j)
							self.person_case_matrix.append([stoks1[i][index] for i in stoks1])
			self.tableWidget_2.setRowCount(len(self.all_data_stoks['name']))
			self.tableWidget_2.setColumnCount(len(self.all_data_stoks.keys()))
			self.fill_table(self.person_case_matrix, True)
			# self.status_label.setText('')
			# self.tableWidget_2.resizeColumnsToContents()

	# МЕТОД ЗАПОЛНЯЮЩИЙ ТАБЛИЦЫ(ТАБЛИЦА ЗАВИСИТ ОТ АРГУМЕНТА)
	def fill_table(self, matrix, case=False):
		matrix = [i[:-1] for i in matrix]
		if case:
			table = self.tableWidget_2
		else:
			table = self.tableWidget
		table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		table.setRowCount(0)
		table.setRowCount(len(matrix))
		table.setMouseTracking(True)
		table.cellClicked.connect(self.stock_info)
		table.cellEntered.connect(self.entered_row_column)
		table.setHorizontalHeaderLabels(list(self.all_data_stoks.keys())[:-1] + ['Добавить/удалить'])
		[table.horizontalHeaderItem(
			i).setFont(QFont('Arial', config.HEAD_SIZE_TABLE)) for i in range(
			len(list(self.all_data_stoks.keys())[:-1] + ['Добавить/удалить']))]
		if self.db.login_exists(LOGIN) and self.db.check_password(LOGIN, PASSWORD):
			person_case = [i[0] for i in self.db.get_case(LOGIN)]
		else:
			person_case = []
		sizes = [400, 100, 120, 120, 120, 120, 120, 170, 120, 100, 100, 100]
		for i, row in enumerate(matrix):
			self.btn = QPushButton(table)
			self.btn.resize(50, 20)
			if row:
				stonk_name = row[0]
				stok_country = row[8]
				if stonk_name in person_case:
					self.btn.setText('❌')
				else:
					self.btn.setText('✅')
				self.btn.setFont(QFont('Arial', config.WORD_SIZE_TABLE))
				self.btn.clicked.connect(partial(self.add_stonk, stonk_name, stok_country))
			for j, col in enumerate(row):
				table.setColumnWidth(j, sizes[j])
				# print(col, j, i)
				item = QTableWidgetItem()
				item.setData(Qt.EditRole, col)
				table.setItem(i, j, item)
				if str(col)[0] == '-':
					table.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
				elif (j == 3 and str(col)[0] != '−') or (j == 2 and str(col)[0] != '−'):
					table.item(i, j).setForeground(QtGui.QBrush(QtGui.QColor(0, 140, 50)))
			table.setCellWidget(i, 10, self.btn)
		table.setColumnWidth(10, 100)

	# МЕТОД ЗАПОЛНЯЮЩИЙ ТАБЛИЦУ С УВЕДОМЛЕНИЯМИ
	def fill_table_notif(self):
		table = self.tableWidget_3
		table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		table.setHorizontalHeaderLabels(['Уведомление❗️', 'Время🕓', 'Дата📅', 'Удалить🗑'])
		[table.horizontalHeaderItem(i).setFont(QFont('Arial', config.HEAD_SIZE_TABLE)) for i in range(4)]
		if self.db.login_exists_notification(LOGIN) and self.db.check_password_notification(LOGIN, PASSWORD):
			person_notification = self.db.get_notifications(LOGIN)
		else:
			person_notification = []
		table.setRowCount(len(person_notification))
		person_notification = [[i[0], i[1].time(), i[1].date()] for i in person_notification]
		person_notification = sorted(person_notification, key=lambda x: (x[2], x[1]), reverse=True)
		for i, row in enumerate(person_notification):
			btn = QPushButton(table)
			btn.resize(50, 20)
			btn.setText('❌')
			btn.setFont(QFont('Arial', config.WORD_SIZE_TABLE))
			item = QTableWidgetItem()
			item.setData(Qt.EditRole, row[0])
			table.setItem(i, 0, item)
			item = QTableWidgetItem()
			item.setData(Qt.EditRole, row[1].strftime("%H:%M:%S"))
			table.setItem(i, 1, item)
			item = QTableWidgetItem()
			item.setData(Qt.EditRole, row[2].strftime("%d.%m.%Y"))
			table.setItem(i, 2, item)
			table.setCellWidget(i, 3, btn)
			date_time_ = dt.combine(row[2], row[1])
			btn.clicked.connect(partial(self.db.delete_notification, LOGIN, date_time_))
			btn.clicked.connect(self.fill_table_notif)

		table.setColumnWidth(0, 1000)
		table.setColumnWidth(1, 120)
		table.setColumnWidth(2, 150)
		table.setColumnWidth(3, 150)

	# МЕТОД ДЛЯ ПОИСКА АКЦИИ НА ГЛАВНОЙ СТРАНИЦЕ
	def search_content(self, case=False):
		if case:
			matrix = []
			search_query = self.search_bar_2.text().lower()
			unification_stoks1 = self.unification_stoks1
			person_unification_stoks1 = []
			for i in self.person_case_matrix:
				unification_stoks1[i[0].lower()] = i
				unification_stoks1[i[1].lower()] = i
				person_unification_stoks1.append(i[0].lower())
				person_unification_stoks1.append(i[1].lower())
			for stok in self.unification_stoks1:
				if (search_query in stok or stok in search_query) and (self.unification_stoks1[stok] not in matrix) \
						and self.unification_stoks1[stok][0] and stok in person_unification_stoks1:
					matrix.append(self.unification_stoks1[stok])
			self.fill_table(matrix, True)
		else:
			matrix = []
			search_query = self.search_bar.text().lower()
			for stok in self.unification_stoks1:
				if (search_query in stok or stok in search_query) and (self.unification_stoks1[stok] not in matrix):
					matrix.append(self.unification_stoks1[stok])
			self.fill_table(matrix)

	# МЕТОД ДЛЯ РЕСТРУКТУРИРОВАНИЯ ДАННЫХ
	def unification_stoks(self):
		unification_stoks1 = {}
		unification_stoks2 = {}
		for i in range(len(self.all_data_stoks['name'])):
			unification_stoks2[
				self.all_data_stoks['name'][i]] = [
				m[i] for m in [self.all_data_stoks[k] for k in self.all_data_stoks]]
			unification_stoks1[
				self.all_data_stoks['name'][i].strip().lower()] = [
				m[i] for m in [self.all_data_stoks[k] for k in self.all_data_stoks]]
			unification_stoks1[
				self.all_data_stoks['logoId'][i].strip().lower()] = [
				m[i] for m in [self.all_data_stoks[k] for k in self.all_data_stoks]]
		self.unification_stoks1 = unification_stoks1
		self.unification_stoks2 = unification_stoks2

	# МЕТОД ДЛЯ СОХРАНЕНИЯ ДАННЫХ С САЙТА В ГЛОБАЛЬНУЮ ПЕРЕМЕННУЮ
	def save_all_data(self, country1):
		global all_data_stoks1, search_flag, progress_bar_val, progress_bar
		all_stonks_from_investing1 = []
		for i in range(len(country1)):
			progress_bar_val = int(100 / len(country1) * (i + 1))
			self.thread_signal.emit(progress_bar_val)
			all_stonks_from_investing1.append(stoks([country1[i]]))

		all_stonks_dict = {}
		for i in all_stonks_from_investing1:
			for key in i:
				all_stonks_dict[key] = all_stonks_dict.get(key, []) + i[key]
		all_data_stoks1 = all_stonks_dict
		search_flag = False
		return all_stonks_dict


def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
	sys.excepthook = except_hook
	App = QApplication(sys.argv)
	sys.excepthook = except_hook
	window = BaseWindow(['russia', ''])
	sys.exit(App.exec())
