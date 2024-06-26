﻿«Система мониторинга и анализа акций»
1. # **Наименование и назначение**
Программное средство TradingView.exe предназначено для сбора и анализа информации об акциях с мировых фондовых рынков, просмотра биржевых новостей, а также формирования и ведения индивидуальных инвестиционных портфелей.
1. # **Авторы проекты**
Проект выполнил ученик МАОУ лицея № 131 Смирнов Максим.
1. # **Идея проекта**
Создание программного продукта для удобного мониторинга рынка акций, формирования индивидуального инвестиционного портфеля и просмотра биржевых новостей.
1. # **Реализация**
Приложение состоит из множества окон, для каждого был создан отдельный класс. В каждом классе описаны методы для взаимодействия пользователя с интерфейсом, а также его дизайн.

Для получения данных с мировых фондовых рынков были написаны функции, их выполнение сопровождается индикатором (progress bar). Эти функции вызываются автоматически через равные промежутки времени (их можно настроить). В качестве источника информации был выбран сайт [TradingView](https://ru.tradingview.com/). Из данных, полученных в процессе “сбора” формируется несколько таблиц, каждая из которых обладает функцией динамической загрузки, это ускоряет работу интерфейса и уменьшает нагрузку на железо компьютера.

После регистрации или входа в личный кабинет у пользователя появляется возможность формировать собственный портфель акций данные которого хранятся и управляются СУБД [PostgressSQL](https://ru.wikipedia.org/wiki/PostgreSQL). Также система предоставляет возможность настроить тему приложения (это можно сделать в настройках)

1. # **Технологии и библиотеки**
Использовались следующие библиотеки (Полный список есть в файле requirements.txt):

- PyQT5 и pyqt5-tools(designer)
- plyer
- psycopg2
- requests
- Pillow

Для создания проекта были освоены следующие технологии:

- Создание [веб-скрепера](https://ru.wikipedia.org/wiki/Веб-скрейпинг) или парсера для сбора данных с внешнего источника (сайта)
- Работа с СУБД Postgress SQL и SQL запросами
- Основы языка программирования Python
- Создание графического интерфейса при помощи библиотеки PyQt5

![C:\Users\MAXX\AppData\Local\Microsoft\Windows\INetCache\Content.Word\снимок экрана.png](Aspose.Words.6e07a54b-ac1c-4e47-904b-87a187e7503d.001.png)

1*Главная страница приложения*

![](Aspose.Words.6e07a54b-ac1c-4e47-904b-87a187e7503d.002.png)

2*Настройки*

![](Aspose.Words.6e07a54b-ac1c-4e47-904b-87a187e7503d.003.png)

3*Данные акции*
