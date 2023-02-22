# ФУНКЦИЯ ДЛЯ ПРОВЕРКИ КОРРЕКТНОСТИ ПАРОЛЯ
def check_password(num: str):
	try:
		assert len(num) >= 8
	except AssertionError:
		return 'Пароль должен содержать 8 или более символов'
	up = False
	low = False
	dig = False
	for k, i in enumerate(num):
		if i.islower():
			low = True
		if i.isupper():
			up = True
		if i.isdigit():
			dig = True
	try:
		assert up == low is True
	except AssertionError:
		return 'В пароле должны присутствовать большие и маленькие буквы'

	try:
		assert dig
	except AssertionError:
		return 'В пароле должны присутствовать цифры'

	return 'ok'


if __name__ == '__main__':
	print(check_password(input()))