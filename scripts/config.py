from os import walk

# Время между обновлением портфеля
MINUT_SAVE_CASE = 10
MINUT_SAVE_ALL = 1

# СПИСОК ДОСТУПНЫХ ТЕМ
themes = [i[:-4] for i in next(walk('themes'), (None, None, []))[2]]

# СПИСОК ССЫЛОК НА АКЦИИ
urls1 = [
	'/markets/stocks-usa/market-movers-active/',
	'/markets/stocks-argentina/market-movers-active/',
	'/markets/stocks-bahrain/market-movers-active/',
	'/markets/stocks-belgium/market-movers-active/',
	'/markets/stocks-brazil/market-movers-active/',
	'/markets/stocks-united-kingdom/market-movers-active/',
	'/markets/stocks-hungary/market-movers-active/',
	'/markets/stocks-venezuela/market-movers-active/',
	'/markets/stocks-vietnam/market-movers-active/',
	'/markets/stocks-germany/market-movers-active/',
	'/markets/stocks-hong-kong/market-movers-active/',
	'/markets/stocks-greece/market-movers-active/',
	'/markets/stocks-denmark/market-movers-active/',
	'/markets/stocks-egypt/market-movers-active/',
	'/markets/stocks-israel/market-movers-active/',
	'/markets/stocks-india/market-movers-active/',
	'/markets/stocks-indonesia/market-movers-active/',
	'/markets/stocks-iceland/market-movers-active/',
	'/markets/stocks-spain/market-movers-active/',
	'/markets/stocks-italy/market-movers-active/',
	'/markets/stocks-canada/market-movers-active/',
	'/markets/stocks-qatar/market-movers-active/',
	'/markets/stocks-china/market-movers-active/',
	'/markets/stocks-colombia/market-movers-active/',
	'/markets/stocks-latvia/market-movers-active/',
	'/markets/stocks-lithuania/market-movers-active/',
	'/markets/stocks-luxembourg/market-movers-active/',
	'/markets/stocks-malaysia/market-movers-active/',
	'/markets/stocks-mexico/market-movers-active/',
	'/markets/stocks-nigeria/market-movers-active/',
	'/markets/stocks-netherlands/market-movers-active/',
	'/markets/stocks-new-zealand/market-movers-active/',
	'/markets/stocks-norway/market-movers-active/',
	'/markets/stocks-uae/market-movers-active/',
	'/markets/stocks-peru/market-movers-active/',
	'/markets/stocks-poland/market-movers-active/',
	'/markets/stocks-portugal/market-movers-active/',
	'/markets/stocks-russia/market-movers-active/',
	'/markets/stocks-romania/market-movers-active/',
	'/markets/stocks-ksa/market-movers-active/',
	'/markets/stocks-serbia/market-movers-active/',
	'/markets/stocks-singapore/market-movers-active/',
	'/markets/stocks-slovakia/market-movers-active/',
	'/markets/stocks-thailand/market-movers-active/',
	'/markets/stocks-taiwan/market-movers-active/',
	'/markets/stocks-turkey/market-movers-active/',
	'/markets/stocks-philippines/market-movers-active/',
	'/markets/stocks-finland/market-movers-active/',
	'/markets/stocks-france/market-movers-active/',
	'/markets/stocks-chile/market-movers-active/',
	'/markets/stocks-switzerland/market-movers-active/',
	'/markets/stocks-sweden/market-movers-active/',
	'/markets/stocks-estonia/market-movers-active/',
	'/markets/stocks-south-africa/market-movers-active/',
	'/markets/stocks-korea/market-movers-active/',
	'/markets/stocks-japan/market-movers-active/'
]

# СПИСОК СТРАН
country = [
	'america', 'argentina', 'bahrain', 'belgium',
	'brazil', 'uk', 'hungary', 'venezuela',
	'vietnam', 'germany', 'hongkong', 'greece',
	'denmark', 'egypt', 'israel', 'india',
	'indonesia', 'iceland', 'spain', 'italy',
	'canada', 'qatar', 'china', 'colombia',
	'latvia', 'lithuania', 'luxembourg', 'malaysia',
	'mexico', 'nigeria', 'netherlands', 'newzealand',
	'norway', 'uae', 'peru', 'poland',
	'portugal', 'russia', 'romania', 'ksa',
	'serbia', 'singapore', 'slovakia', 'thailand',
	'taiwan', 'turkey', 'philippines', 'finland',
	'france', 'chile', 'switzerland', 'sweden',
	'estonia', 'rsa', 'korea', 'japan']

# ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ(2 ВАРИАНТА ТАК КАК 2 СЕРВЕРА)
user = "dwadqzzicgirat"
password = "d474b4ba3c35ce84079fae4fb5db7dd7afd6ee2d4238c34e565b58b3929a2c4c"
host = "ec2-54-228-32-29.eu-west-1.compute.amazonaws.com"
port = "5432"
database = "d8fbncnt2b47h4"

user1 = "iabgfrdq"
password1 = "NJziiODla1yj4DGkTJ2DZu4_ioSQCh0J"
host1 = "mouse.db.elephantsql.com"
port1 = "5432"
database1 = "iabgfrdq"

# РАЗМЕР ШРИФТОВ
WORD_SIZE_TABLE = 12
HEAD_SIZE_TABLE = 9
